import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  SparklesIcon,
  CpuChipIcon,
  ShieldCheckIcon,
  ChartBarIcon,
  GlobeAltIcon,
  BoltIcon,
  FireIcon,
  CloudIcon,
  UserGroupIcon,
  HeartIcon,
  ArrowRightIcon,
  PlayIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'

const LandingPage = ({ onNavigate }) => {
  const [currentFeature, setCurrentFeature] = useState(0)
  const [particles, setParticles] = useState([])

  const features = [
    {
      icon: CpuChipIcon,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning algorithms analyze emergency patterns and predict flood risks with 97% accuracy",
      color: "text-blue-400"
    },
    {
      icon: ShieldCheckIcon,
      title: "Real-time Monitoring",
      description: "24/7 monitoring of IoT sensors and emergency channels for instant response to crisis situations",
      color: "text-green-400"
    },
    {
      icon: ChartBarIcon,
      title: "Predictive Analytics",
      description: "Early warning system that predicts natural disasters up to 6 hours in advance",
      color: "text-purple-400"
    },
    {
      icon: GlobeAltIcon,
      title: "Multi-Platform Support",
      description: "Seamless integration with Telegram, WhatsApp, and direct API for maximum accessibility",
      color: "text-yellow-400"
    }
  ]

  const stats = [
    { label: "Cities Covered", value: "20+", icon: GlobeAltIcon },
    { label: "Population Protected", value: "150M+", icon: UserGroupIcon },
    { label: "Response Time", value: "2.3 min", icon: BoltIcon },
    { label: "Success Rate", value: "98.5%", icon: CheckCircleIcon }
  ]

  const testimonials = [
    {
      name: "Dr. Rajesh Kumar",
      role: "Emergency Response Director",
      location: "Mumbai",
      quote: "JalRakshā AI has revolutionized our emergency response capabilities. The AI predictions have saved countless lives.",
      avatar: "👨‍⚕️"
    },
    {
      name: "Priya Sharma",
      role: "Disaster Management Officer",
      location: "Chennai",
      quote: "The real-time monitoring and early warning system has been a game-changer for our city's safety.",
      avatar: "👩‍💼"
    },
    {
      name: "Amit Patel",
      role: "Rescue Team Leader",
      location: "Kolkata",
      quote: "The multi-platform integration allows us to reach people through their preferred communication channels.",
      avatar: "👨‍🚒"
    }
  ]

  useEffect(() => {
    // Create floating particles
    const newParticles = Array.from({ length: 50 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 4 + 2,
      delay: Math.random() * 6
    }))
    setParticles(newParticles)

    // Auto-rotate features
    const interval = setInterval(() => {
      setCurrentFeature((prev) => (prev + 1) % features.length)
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 relative overflow-hidden">
      {/* Floating Particles */}
      <div className="absolute inset-0 pointer-events-none">
        {particles.map((particle) => (
          <motion.div
            key={particle.id}
            className="absolute bg-white/10 rounded-full"
            style={{
              left: `${particle.x}%`,
              top: `${particle.y}%`,
              width: `${particle.size}px`,
              height: `${particle.size}px`
            }}
            animate={{
              y: [-20, 20, -20],
              opacity: [0.3, 0.8, 0.3]
            }}
            transition={{
              duration: 6,
              repeat: Infinity,
              delay: particle.delay
            }}
          />
        ))}
      </div>

      {/* Hero Section */}
      <section className="relative z-10 py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
              className="inline-flex items-center space-x-3 mb-8"
            >
              <SparklesIcon className="h-12 w-12 text-blue-400" />
              <h1 className="text-6xl md:text-8xl font-black text-white">
                JalRakshā AI
              </h1>
            </motion.div>
            
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="text-2xl md:text-3xl text-blue-100 mb-8 max-w-4xl mx-auto"
            >
              AI + IoT Powered Flood & Disaster Early Warning & Rescue System
            </motion.p>
            
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <button
                onClick={() => onNavigate('dashboard')}
                className="group bg-white text-blue-600 px-8 py-4 rounded-full font-bold hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-2xl flex items-center justify-center space-x-2"
              >
                <span>🚀 Open Dashboard</span>
                <ArrowRightIcon className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </button>
              
              <button
                onClick={() => onNavigate('sos')}
                className="group bg-red-500 text-white px-8 py-4 rounded-full font-bold hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-2xl flex items-center justify-center space-x-2"
              >
                <span>🚨 Emergency SOS</span>
                <PlayIcon className="h-5 w-5 group-hover:scale-110 transition-transform" />
              </button>
            </motion.div>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-20"
          >
            {stats.map((stat, index) => {
              const Icon = stat.icon
              return (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.9 + index * 0.1 }}
                  className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 text-center hover:scale-105 transition-transform"
                >
                  <Icon className="h-8 w-8 text-blue-400 mx-auto mb-3" />
                  <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
                  <div className="text-sm text-gray-400">{stat.label}</div>
                </motion.div>
              )
            })}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="relative z-10 py-20 px-6 bg-gray-900/30">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Advanced AI Technology
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Cutting-edge artificial intelligence and IoT sensors working together to protect communities
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Feature Display */}
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="relative"
            >
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 border border-gray-700 h-80 flex items-center justify-center">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={currentFeature}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.8 }}
                    className="text-center"
                  >
                    <features[currentFeature].icon className={`h-16 w-16 ${features[currentFeature].color} mx-auto mb-4`} />
                    <h3 className="text-2xl font-bold text-white mb-2">
                      {features[currentFeature].title}
                    </h3>
                    <p className="text-gray-300">
                      {features[currentFeature].description}
                    </p>
                  </motion.div>
                </AnimatePresence>
              </div>
            </motion.div>

            {/* Feature List */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
              className="space-y-6"
            >
              {features.map((feature, index) => {
                const Icon = feature.icon
                return (
                  <motion.div
                    key={feature.title}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                    className={`p-6 rounded-xl border transition-all cursor-pointer ${
                      currentFeature === index
                        ? 'bg-blue-900/30 border-blue-500'
                        : 'bg-gray-800/30 border-gray-700 hover:border-gray-600'
                    }`}
                    onClick={() => setCurrentFeature(index)}
                  >
                    <div className="flex items-center space-x-4">
                      <Icon className={`h-8 w-8 ${feature.color}`} />
                      <div>
                        <h3 className="text-lg font-semibold text-white">
                          {feature.title}
                        </h3>
                        <p className="text-gray-400 text-sm">
                          {feature.description}
                        </p>
                      </div>
                    </div>
                  </motion.div>
                )
              })}
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="relative z-10 py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Trusted by Emergency Teams
            </h2>
            <p className="text-xl text-gray-300">
              Real stories from emergency response professionals across India
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + index * 0.1 }}
                className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-8 border border-gray-700 hover:scale-105 transition-transform"
              >
                <div className="text-center mb-6">
                  <div className="text-4xl mb-4">{testimonial.avatar}</div>
                  <h3 className="text-xl font-bold text-white">{testimonial.name}</h3>
                  <p className="text-blue-400">{testimonial.role}</p>
                  <p className="text-gray-400 text-sm">{testimonial.location}</p>
                </div>
                <blockquote className="text-gray-300 italic">
                  "{testimonial.quote}"
                </blockquote>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative z-10 py-20 px-6 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <HeartIcon className="h-16 w-16 text-white mx-auto mb-6" />
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Protect Your Community?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Join thousands of emergency responders using JalRakshā AI to save lives
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={() => onNavigate('dashboard')}
                className="bg-white text-blue-600 px-8 py-4 rounded-full font-bold hover:scale-105 transition-all duration-300 shadow-lg"
              >
                Start Monitoring Now
              </button>
              <button
                onClick={() => onNavigate('sos')}
                className="bg-transparent border-2 border-white text-white px-8 py-4 rounded-full font-bold hover:bg-white hover:text-blue-600 transition-all duration-300"
              >
                Emergency Access
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 py-12 px-6 bg-gray-900/50">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            <div className="flex items-center justify-center space-x-3 mb-6">
              <SparklesIcon className="h-8 w-8 text-blue-400" />
              <h3 className="text-2xl font-bold text-white">JalRakshā AI</h3>
            </div>
            <p className="text-gray-400 mb-6">
              AI + IoT Powered Flood & Disaster Early Warning & Rescue Management
            </p>
            <div className="flex justify-center space-x-6 text-sm">
              <button
                onClick={() => onNavigate('dashboard')}
                className="text-gray-400 hover:text-white transition-colors"
              >
                Dashboard
              </button>
              <button
                onClick={() => onNavigate('sos')}
                className="text-gray-400 hover:text-white transition-colors"
              >
                SOS System
              </button>
              <button
                onClick={() => onNavigate('analytics')}
                className="text-gray-400 hover:text-white transition-colors"
              >
                Analytics
              </button>
            </div>
          </motion.div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage

