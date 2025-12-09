# Security Policy

## 🔒 Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## 🛡️ Security Features

### **Data Privacy**
- ✅ **100% Local Processing:** All AI inference, vector search, and data processing happens locally
- ✅ **No External API Calls:** No data sent to third-party services (OpenAI, Google, etc.)
- ✅ **Local Storage:** Vector database (ChromaDB) and SQLite database stored locally
- ✅ **Browser-based Conversations:** Chat history stored in browser (clearable)
- ✅ **No Tracking:** No analytics, telemetry, or user tracking
- ✅ **Open Source:** Fully auditable codebase

### **Authentication & Authorization**
- ⚠️ **Development:** No authentication (for local development only)
- ✅ **Production:** Implement JWT-based authentication before deployment
- ✅ **Role-Based Access Control (RBAC):** Planned for production

### **Input Validation**
- ✅ **Pydantic Validation:** All API inputs validated with Pydantic v2
- ✅ **SQL Injection Protection:** SQLAlchemy ORM prevents SQL injection
- ✅ **XSS Protection:** React sanitizes HTML by default
- ✅ **CORS Configuration:** Restrict origins in production

### **Dependencies**
- ✅ **Regular Updates:** Dependencies updated regularly
- ✅ **Vulnerability Scanning:** Automated scanning via Dependabot (GitHub)
- ✅ **Minimal Dependencies:** Only essential packages included

---

## 🚨 Reporting a Vulnerability

**We take security seriously!** If you discover a security vulnerability, please follow responsible disclosure:

### **DO:**
✅ **Email us privately:** security@yourproject.com  
✅ **Provide detailed information:**
  - Description of the vulnerability
  - Steps to reproduce
  - Potential impact
  - Suggested fix (if available)
✅ **Wait for acknowledgment** before public disclosure (we aim to respond within 48 hours)

### **DON'T:**
❌ **DO NOT** create public GitHub issues for security vulnerabilities  
❌ **DO NOT** exploit the vulnerability maliciously  
❌ **DO NOT** disclose publicly until we've had time to fix it (typically 90 days)

### **Response Timeline:**
- **Initial Response:** Within 48 hours
- **Status Update:** Within 7 days
- **Fix & Disclosure:** Within 90 days (or as agreed upon)

### **Rewards:**
We currently don't have a bug bounty program, but we will:
- ✅ Acknowledge you in the CHANGELOG (unless you prefer anonymity)
- ✅ Add you to our CONTRIBUTORS list
- ✅ Provide public recognition (with your permission)

---

## 🔐 Security Best Practices

### **For Development:**

1. **Environment Variables:**
   ```bash
   # .env file (NEVER commit to git)
   SECRET_KEY=your-secret-key-here
   DEBUG=true
   ALLOWED_ORIGINS=http://localhost:5173
   ```

2. **Virtual Environment:**
   ```bash
   # Always use virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate   # Windows
   ```

3. **Dependencies:**
   ```bash
   # Keep dependencies updated
   pip list --outdated
   pip install --upgrade package-name
   ```

### **For Production Deployment:**

1. **Environment Variables:**
   ```bash
   # Production .env
   SECRET_KEY=$(openssl rand -hex 32)  # Strong random key
   DEBUG=false
   ALLOWED_ORIGINS=https://yourdomain.com
   DATABASE_URL=postgresql://user:pass@localhost/db
   ```

2. **HTTPS/TLS:**
   - ✅ Use Let's Encrypt for free SSL certificates
   - ✅ Redirect HTTP to HTTPS
   - ✅ Set `Strict-Transport-Security` header

3. **Database:**
   - ✅ Use PostgreSQL (not SQLite) for production
   - ✅ Enable SSL for database connections
   - ✅ Regular backups with encryption

4. **CORS Configuration:**
   ```python
   # backend/app/core/config.py
   ALLOWED_ORIGINS = [
       "https://yourdomain.com",
       "https://www.yourdomain.com",
   ]
   ```

5. **Rate Limiting:**
   ```python
   # Install slowapi
   pip install slowapi
   
   # Add rate limiting to endpoints
   from slowapi import Limiter, _rate_limit_exceeded_handler
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/api/v1/chat")
   @limiter.limit("10/minute")
   async def chat(request: Request, ...):
       ...
   ```

6. **Security Headers:**
   ```python
   # backend/app/main.py
   from fastapi.middleware.trustedhost import TrustedHostMiddleware
   from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
   
   app.add_middleware(HTTPSRedirectMiddleware)
   app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])
   
   @app.middleware("http")
   async def add_security_headers(request: Request, call_next):
       response = await call_next(request)
       response.headers["X-Content-Type-Options"] = "nosniff"
       response.headers["X-Frame-Options"] = "DENY"
       response.headers["X-XSS-Protection"] = "1; mode=block"
       response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
       return response
   ```

7. **Logging & Monitoring:**
   - ✅ Log all authentication attempts
   - ✅ Monitor for suspicious activity
   - ✅ Set up alerts for errors
   - ✅ Use centralized logging (ELK stack, Splunk, etc.)

8. **Regular Updates:**
   ```bash
   # Check for vulnerabilities
   pip-audit  # Install: pip install pip-audit
   npm audit  # For frontend
   
   # Update dependencies
   pip install --upgrade -r requirements.txt
   npm update
   ```

---

## 🔍 Known Security Considerations

### **1. Local LLM (Ollama/Mistral)**
- **Risk:** Model inference runs locally, consuming system resources
- **Mitigation:** Monitor resource usage, implement request queuing
- **Note:** No external API calls = No data leakage to third parties

### **2. SQLite (Development)**
- **Risk:** Not suitable for concurrent writes, production workloads
- **Mitigation:** Use PostgreSQL for production deployment
- **Note:** Fine for development and single-user deployments

### **3. ChromaDB (Vector Database)**
- **Risk:** Local storage, no built-in encryption
- **Mitigation:** Encrypt disk, use file system encryption (LUKS, BitLocker)
- **Note:** Data is local, not transmitted externally

### **4. No Authentication (Development)**
- **Risk:** Anyone with access can use the API
- **Mitigation:** Implement JWT-based auth before deployment
- **Note:** Intended for local development only

### **5. CORS (Development)**
- **Risk:** Allows all origins in development
- **Mitigation:** Restrict to specific domains in production
- **Note:** Configured in `backend/app/core/config.py`

### **6. Debug Mode (Development)**
- **Risk:** Exposes stack traces and internal errors
- **Mitigation:** Set `DEBUG=false` in production
- **Note:** Useful for development, dangerous in production

### **7. Sensitive Data in Logs**
- **Risk:** User queries may contain sensitive information
- **Mitigation:** Implement log sanitization, PII redaction
- **Note:** Consider GDPR/data protection compliance

### **8. Model Hallucinations**
- **Risk:** AI may generate incorrect legal guidance
- **Mitigation:** Always verify with official sources
- **Note:** Disclaimers added to all responses

---

## 🛠️ Security Tools & Automation

### **Automated Scanning:**

1. **Dependabot (GitHub):**
   - Automatically checks for vulnerable dependencies
   - Creates PRs for updates
   - Enable in `.github/dependabot.yml`

2. **CodeQL (GitHub):**
   - Scans code for security vulnerabilities
   - Enable in repository settings → Security → Code scanning

3. **Python Security:**
   ```bash
   # Install security tools
   pip install bandit safety pip-audit
   
   # Run scans
   bandit -r backend/app/  # Static analysis
   safety check            # Dependency vulnerabilities
   pip-audit               # Audit dependencies
   ```

4. **Frontend Security:**
   ```bash
   # Audit npm packages
   npm audit
   npm audit fix  # Auto-fix vulnerabilities
   ```

---

## 📜 Compliance & Regulations

### **India-Specific:**
- **IT Act 2000:** Information Technology Act (cybercrime laws)
- **IT Rules 2021:** Intermediary Guidelines and Digital Media Ethics Code
- **Personal Data Protection Bill (PDPB):** Upcoming data protection law
- **CERT-In Directions 2022:** Incident reporting requirements (6 hours)

### **International:**
- **GDPR (EU):** General Data Protection Regulation (if serving EU users)
- **CCPA (California):** California Consumer Privacy Act (if serving CA users)
- **ISO 27001:** Information security management (recommended)

### **Data Handling:**
- ✅ **Local Processing:** Compliant with data localization requirements
- ✅ **No Third-Party Sharing:** No data sent to external services
- ✅ **User Control:** Users can clear chat history anytime
- ✅ **Transparency:** Open-source code is fully auditable

---

## 📞 Security Contact

**Primary Contact:** security@yourproject.com  
**GitHub Security Advisories:** https://github.com/brittytino/cyber-sop-assistant/security/advisories  
**PGP Key:** (Optional: Add your PGP public key for encrypted communication)

**Response Time:**
- Critical: 24 hours
- High: 48 hours
- Medium: 7 days
- Low: 14 days

---

## 🏆 Security Hall of Fame

We acknowledge and thank the following security researchers:

*(No reports yet - be the first!)*

---

## 📚 Resources

- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **CWE Top 25:** https://cwe.mitre.org/top25/
- **CERT-In Guidelines:** https://www.cert-in.org.in
- **IT Act 2000:** https://www.meity.gov.in/content/information-technology-act
- **FastAPI Security:** https://fastapi.tiangolo.com/tutorial/security/
- **React Security:** https://reactjs.org/docs/dom-elements.html#dangerouslysetinnerhtml

---

**Last Updated:** December 2024  
**Version:** 1.0.0

**Stay Safe! 🛡️**
