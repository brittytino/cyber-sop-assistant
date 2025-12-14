"""
Chat Router - Handles chat conversations and RAG queries
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging


from ..dependencies import get_db
from ..schemas import ChatMessageRequest, ChatMessageResponse, ChatOut, ChatListItem, ChatCreate
from ..models import Chat, Message, User
from .auth import get_current_user
# from ..services.rag import answer_query # Removed unused import


logger = logging.getLogger(__name__)

router = APIRouter()

from fastapi.responses import StreamingResponse
from ..services.rag import answer_query_stream


@router.post("/message")
async def send_message(request: ChatMessageRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Send a message and get AI response with RAG (Streaming)
    """
    try:
        # Get or create chat
        if request.chat_id:
            chat = db.query(Chat).filter(Chat.id == request.chat_id, Chat.user_id == current_user.id).first()
            if not chat:
                raise HTTPException(status_code=404, detail="Chat not found or access denied")
        else:
            # Create new chat
            title = request.message[:50] + "..." if len(request.message) > 50 else request.message
            chat = Chat(title=title, user_id=current_user.id)
            db.add(chat)
            db.commit()
            db.refresh(chat)
            logger.info(f"Created new chat: {chat.id} for user {current_user.username}")
        
        # Save user message
        user_message_content = request.message
        extra_context = ""
        
        # Handle Image/OCR
        if request.image:
            try:
                import base64
                from ..services.ocr import extract_text_from_image
                
                # Check if it has a header like "data:image/png;base64,"
                image_data = request.image
                if "," in image_data:
                    image_data = image_data.split(",")[1]
                
                image_bytes = base64.b64decode(image_data)
                ocr_text = extract_text_from_image(image_bytes)
                if ocr_text:
                    extra_context = ocr_text
                    # Append OCR text to the content that will be saved to DB
                    user_message_content += f"\n\n[Image Content: {ocr_text}]"
                    
                    # Add specific instruction for fraud analysis if image is present
                    extra_context += "\n\n[SYSTEM NOTE: The user has uploaded an image. The content above is extracted via OCR. Please ANALYZE this text specifically for potential SCAMS, FRAUD, or PHISHING indicators. If it looks like a scam, warn the user immediately and explain why.]"
                    
                    logger.info(f"Extracted OCR text: {ocr_text[:50]}...")
            except Exception as e:
                logger.error(f"Error processing image: {e}")
        
        # Detect Language
        language = request.language
        if not language:
            try:
                from langdetect import detect
                # Detect from message + extra_context
                text_to_detect = request.message + " " + extra_context
                lang_code = detect(text_to_detect)
                lang_map = {
                    "hi": "Hindi",
                    "ta": "Tamil",
                    "te": "Telugu",
                    "ml": "Malayalam",
                    "mr": "Marathi",
                    "kn": "Kannada",
                    "bn": "Bengali",
                    "gu": "Gujarati",
                    "en": "English"
                }
                language = lang_map.get(lang_code, "English")
                logger.info(f"Detected language: {language} ({lang_code})")
            except:
                language = "English"

        user_message = Message(
            chat_id=chat.id,
            role="user",
            content=user_message_content,
            language=language
        )
        db.add(user_message)
        db.commit()

        # Generator to stream response AND save to DB
        async def stream_and_save(chat_id: int):
            full_response = ""
            import json
            
            # Helper to save
            def save_assistant_message(text: str):
                try:
                    # Create new session for background save (since original might be closed or in different state)
                    from ..db import SessionLocal
                    db_bg = SessionLocal()
                    
                    asst_msg = Message(
                        chat_id=chat_id,
                        role="assistant",
                        content=text,
                    )
                    db_bg.add(asst_msg)
                    # Update chat timestamp
                    chat_ref = db_bg.query(Chat).filter(Chat.id == chat_id).first()
                    if chat_ref:
                        from datetime import datetime
                        chat_ref.updated_at = datetime.utcnow()
                        
                    db_bg.commit()
                    db_bg.close()
                    logger.info(f"Saved assistant message for chat {chat_id}")
                except Exception as ex:
                    logger.error(f"Failed to save assistant message: {ex}")

            # Stream chunks
            for chunk in answer_query_stream(request.message, language=language, extra_context=extra_context, chat_id=chat_id):
                yield chunk
                
                # Parse chunk to accumulate text content
                try:
                    data = json.loads(chunk)
                    if data.get("type") == "content":
                        full_response += data.get("data", "")
                except:
                    pass
            
            # After stream ends, save to DB
            if full_response:
                save_assistant_message(full_response)

        # Return streaming response
        return StreamingResponse(
            stream_and_save(chat.id),
            media_type="application/x-ndjson"
        )
        
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chats", response_model=List[ChatListItem])
async def get_chats(limit: int = 20, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get list of recent chats
    """
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).order_by(Chat.updated_at.desc()).limit(limit).all()
    return chats

@router.get("/chats/{chat_id}", response_model=ChatOut)
async def get_chat(chat_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get a specific chat with all messages
    """
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.post("/chats", response_model=ChatOut)
async def create_chat(chat_data: ChatCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new chat
    """
    chat = Chat(title=chat_data.title, user_id=current_user.id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

@router.delete("/chats/{chat_id}")
async def delete_chat(chat_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete a chat and all its messages
    """
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted successfully"}
