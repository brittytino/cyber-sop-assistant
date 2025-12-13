import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { 
  BookOpen, Play, CheckCircle, X, AlertCircle, ArrowRight,
  Shield, CreditCard, Mail, Smartphone, User, HelpCircle
} from 'lucide-react'

interface Scenario {
  id: string
  category: 'upi_scam' | 'phishing' | 'fake_job' | 'social_media_hack' | 'investment_fraud' | 'identity_theft'
  title: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  description: string
  icon: React.ElementType
}

interface Question {
  id: string
  situation: string
  options: {
    id: string
    text: string
    correct: boolean
    explanation: string
  }[]
}

export default function ScenarioSimulatorPage() {
  const { t } = useTranslation()
  const [selectedScenario, setSelectedScenario] = useState<Scenario | null>(null)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null)
  const [showExplanation, setShowExplanation] = useState(false)
  const [score, setScore] = useState({ correct: 0, total: 0 })

  const scenarios: Scenario[] = [
    {
      id: 'upi_scam',
      category: 'upi_scam',
      title: t('simulator.scenarios.upiScam.title'),
      difficulty: 'beginner',
      description: t('simulator.scenarios.upiScam.description'),
      icon: CreditCard
    },
    {
      id: 'phishing',
      category: 'phishing',
      title: t('simulator.scenarios.phishing.title'),
      difficulty: 'intermediate',
      description: t('simulator.scenarios.phishing.description'),
      icon: Mail
    },
    {
      id: 'fake_job',
      category: 'fake_job',
      title: t('simulator.scenarios.fakeJob.title'),
      difficulty: 'intermediate',
      description: t('simulator.scenarios.fakeJob.description'),
      icon: User
    },
    {
      id: 'social_media_hack',
      category: 'social_media_hack',
      title: t('simulator.scenarios.socialMediaHack.title'),
      difficulty: 'beginner',
      description: t('simulator.scenarios.socialMediaHack.description'),
      icon: Smartphone
    },
    {
      id: 'investment_fraud',
      category: 'investment_fraud',
      title: t('simulator.scenarios.investmentFraud.title'),
      difficulty: 'advanced',
      description: t('simulator.scenarios.investmentFraud.description'),
      icon: Shield
    },
    {
      id: 'identity_theft',
      category: 'identity_theft',
      title: t('simulator.scenarios.identityTheft.title'),
      difficulty: 'advanced',
      description: t('simulator.scenarios.identityTheft.description'),
      icon: AlertCircle
    }
  ]

  // Sample questions (in production, these would come from the backend)
  const getQuestionsForScenario = (scenarioId: string): Question[] => {
    return [
      {
        id: '1',
        situation: t(`simulator.scenarios.${scenarioId}.question1.situation`),
        options: [
          {
            id: 'a',
            text: t(`simulator.scenarios.${scenarioId}.question1.optionA`),
            correct: false,
            explanation: t(`simulator.scenarios.${scenarioId}.question1.explanationA`)
          },
          {
            id: 'b',
            text: t(`simulator.scenarios.${scenarioId}.question1.optionB`),
            correct: true,
            explanation: t(`simulator.scenarios.${scenarioId}.question1.explanationB`)
          },
          {
            id: 'c',
            text: t(`simulator.scenarios.${scenarioId}.question1.optionC`),
            correct: false,
            explanation: t(`simulator.scenarios.${scenarioId}.question1.explanationC`)
          }
        ]
      },
      {
        id: '2',
        situation: t(`simulator.scenarios.${scenarioId}.question2.situation`),
        options: [
          {
            id: 'a',
            text: t(`simulator.scenarios.${scenarioId}.question2.optionA`),
            correct: true,
            explanation: t(`simulator.scenarios.${scenarioId}.question2.explanationA`)
          },
          {
            id: 'b',
            text: t(`simulator.scenarios.${scenarioId}.question2.optionB`),
            correct: false,
            explanation: t(`simulator.scenarios.${scenarioId}.question2.explanationB`)
          },
          {
            id: 'c',
            text: t(`simulator.scenarios.${scenarioId}.question2.optionC`),
            correct: false,
            explanation: t(`simulator.scenarios.${scenarioId}.question2.explanationC`)
          }
        ]
      }
    ]
  }

  const startScenario = (scenario: Scenario) => {
    setSelectedScenario(scenario)
    setCurrentQuestion(0)
    setSelectedAnswer(null)
    setShowExplanation(false)
    setScore({ correct: 0, total: 0 })
  }

  const questions = selectedScenario ? getQuestionsForScenario(selectedScenario.category) : []
  const currentQ = questions[currentQuestion]

  const handleAnswerSelect = (optionId: string) => {
    setSelectedAnswer(optionId)
  }

  const submitAnswer = () => {
    if (!selectedAnswer || !currentQ) return

    const option = currentQ.options.find(o => o.id === selectedAnswer)
    if (option?.correct) {
      setScore(prev => ({ ...prev, correct: prev.correct + 1, total: prev.total + 1 }))
    } else {
      setScore(prev => ({ ...prev, total: prev.total + 1 }))
    }
    setShowExplanation(true)
  }

  const nextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1)
      setSelectedAnswer(null)
      setShowExplanation(false)
    } else {
      // Scenario complete
      setSelectedScenario(null)
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
      case 'advanced':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    }
  }

  if (selectedScenario && questions.length > 0) {
    const progressPercentage = ((currentQuestion + 1) / questions.length) * 100

    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
        {/* Header */}
        <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
          <div className="max-w-4xl mx-auto">
            <button
              onClick={() => setSelectedScenario(null)}
              className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-4"
            >
              <X className="w-5 h-5" />
              {t('simulator.exitScenario')}
            </button>

            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                {selectedScenario.title}
              </h1>
              <div className="text-right">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {t('simulator.question')} {currentQuestion + 1} {t('simulator.of')} {questions.length}
                </p>
                <p className="text-sm font-medium text-indigo-600 dark:text-indigo-400">
                  {t('simulator.score')}: {score.correct}/{score.total}
                </p>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-4">
              <div
                className="bg-indigo-600 h-2 rounded-full transition-all"
                style={{ width: `${progressPercentage}%` }}
              />
            </div>
          </div>
        </div>

        {/* Question */}
        <div className="max-w-4xl mx-auto px-6 py-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
              {currentQ.situation}
            </h2>

            <div className="space-y-4">
              {currentQ.options.map(option => (
                <button
                  key={option.id}
                  onClick={() => !showExplanation && handleAnswerSelect(option.id)}
                  disabled={showExplanation}
                  className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                    selectedAnswer === option.id
                      ? showExplanation
                        ? option.correct
                          ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                          : 'border-red-500 bg-red-50 dark:bg-red-900/20'
                        : 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20'
                      : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                  } ${showExplanation && option.correct ? 'border-green-500 bg-green-50 dark:bg-green-900/20' : ''}`}
                >
                  <div className="flex items-start gap-3">
                    <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                      selectedAnswer === option.id && showExplanation
                        ? option.correct
                          ? 'bg-green-500 text-white'
                          : 'bg-red-500 text-white'
                        : showExplanation && option.correct
                          ? 'bg-green-500 text-white'
                          : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
                    }`}>
                      {showExplanation && option.correct ? <CheckCircle className="w-5 h-5" /> : option.id.toUpperCase()}
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 dark:text-white">{option.text}</p>
                      {showExplanation && selectedAnswer === option.id && (
                        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                          {option.explanation}
                        </p>
                      )}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-between">
            <button
              onClick={() => setSelectedScenario(null)}
              className="bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded-lg px-6 py-3 font-medium transition-colors"
            >
              {t('simulator.exitScenario')}
            </button>
            {!showExplanation ? (
              <button
                onClick={submitAnswer}
                disabled={!selectedAnswer}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white rounded-lg px-6 py-3 font-medium transition-colors disabled:cursor-not-allowed"
              >
                {t('simulator.submitAnswer')}
                <ArrowRight className="w-5 h-5" />
              </button>
            ) : (
              <button
                onClick={nextQuestion}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-6 py-3 font-medium transition-colors"
              >
                {currentQuestion < questions.length - 1 ? t('simulator.nextQuestion') : t('simulator.finish')}
                <ArrowRight className="w-5 h-5" />
              </button>
            )}
          </div>

          {/* Score Summary */}
          {showExplanation && currentQuestion === questions.length - 1 && (
            <div className="mt-6 bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800 rounded-lg p-6 text-center">
              <h3 className="text-lg font-semibold text-indigo-900 dark:text-indigo-200 mb-2">
                {t('simulator.scenarioComplete')}
              </h3>
              <p className="text-indigo-800 dark:text-indigo-300">
                {t('simulator.finalScore')}: {score.correct}/{score.total} ({Math.round((score.correct / score.total) * 100)}%)
              </p>
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-3">
            <BookOpen className="w-8 h-8 text-green-600 dark:text-green-400" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                {t('simulator.title')}
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-1">
                {t('simulator.subtitle')}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Info Card */}
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6 mb-8">
          <div className="flex items-start gap-3">
            <HelpCircle className="w-6 h-6 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-blue-900 dark:text-blue-200 mb-2">
                {t('simulator.howItWorks')}
              </h3>
              <p className="text-sm text-blue-800 dark:text-blue-300">
                {t('simulator.howItWorksDesc')}
              </p>
            </div>
          </div>
        </div>

        {/* Scenarios Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {scenarios.map(scenario => {
            const Icon = scenario.icon
            return (
              <div
                key={scenario.id}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-all overflow-hidden"
              >
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="bg-indigo-100 dark:bg-indigo-900 p-3 rounded-lg">
                      <Icon className="w-8 h-8 text-indigo-600 dark:text-indigo-400" />
                    </div>
                    <span className={`text-xs font-medium px-3 py-1 rounded-full ${getDifficultyColor(scenario.difficulty)}`}>
                      {t(`simulator.difficulty.${scenario.difficulty}`)}
                    </span>
                  </div>

                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {scenario.title}
                  </h3>

                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-6 line-clamp-3">
                    {scenario.description}
                  </p>

                  <button
                    onClick={() => startScenario(scenario)}
                    className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-4 py-2 font-medium transition-colors"
                  >
                    <Play className="w-4 h-4" />
                    {t('simulator.startScenario')}
                  </button>
                </div>
              </div>
            )
          })}
        </div>

        {/* Benefits Section */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <Shield className="w-8 h-8 text-green-600 dark:text-green-400 mb-3" />
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
              {t('simulator.benefits.safe')}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {t('simulator.benefits.safeDesc')}
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <BookOpen className="w-8 h-8 text-blue-600 dark:text-blue-400 mb-3" />
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
              {t('simulator.benefits.learn')}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {t('simulator.benefits.learnDesc')}
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <CheckCircle className="w-8 h-8 text-indigo-600 dark:text-indigo-400 mb-3" />
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
              {t('simulator.benefits.prepared')}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {t('simulator.benefits.preparedDesc')}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
