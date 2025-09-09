/**
 * Theme utilities for JalRakshā AI
 */

/**
 * Risk level color mappings
 */
export const RISK_COLORS = {
  LOW: {
    bg: 'bg-green-500/20',
    text: 'text-green-400',
    border: 'border-green-500/30',
    glow: 'glow-green',
    hex: '#10b981',
  },
  MEDIUM: {
    bg: 'bg-yellow-500/20',
    text: 'text-yellow-400',
    border: 'border-yellow-500/30',
    glow: 'glow-yellow',
    hex: '#f59e0b',
  },
  HIGH: {
    bg: 'bg-red-500/20',
    text: 'text-red-400',
    border: 'border-red-500/30',
    glow: 'glow-red',
    hex: '#ef4444',
  },
}

/**
 * Get risk level colors
 */
export function getRiskColors(riskLevel) {
  return RISK_COLORS[riskLevel?.toUpperCase()] || RISK_COLORS.LOW
}

/**
 * Get risk level CSS classes
 */
export function getRiskClasses(riskLevel) {
  const colors = getRiskColors(riskLevel)
  return `${colors.bg} ${colors.text} ${colors.border}`
}

/**
 * Status color mappings
 */
export const STATUS_COLORS = {
  idle: {
    bg: 'bg-gray-500/20',
    text: 'text-gray-400',
    border: 'border-gray-500/30',
  },
  dispatched: {
    bg: 'bg-blue-500/20',
    text: 'text-blue-400',
    border: 'border-blue-500/30',
  },
  'en-route': {
    bg: 'bg-yellow-500/20',
    text: 'text-yellow-400',
    border: 'border-yellow-500/30',
  },
  completed: {
    bg: 'bg-green-500/20',
    text: 'text-green-400',
    border: 'border-green-500/30',
  },
}

/**
 * Get status colors
 */
export function getStatusColors(status) {
  return STATUS_COLORS[status?.toLowerCase()] || STATUS_COLORS.idle
}

/**
 * Get status CSS classes
 */
export function getStatusClasses(status) {
  const colors = getStatusColors(status)
  return `${colors.bg} ${colors.text} ${colors.border}`
}

/**
 * Animation variants for Framer Motion
 */
export const ANIMATION_VARIANTS = {
  fadeIn: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
  },
  slideUp: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -20 },
  },
  slideDown: {
    initial: { opacity: 0, y: -20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 20 },
  },
  slideLeft: {
    initial: { opacity: 0, x: 20 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -20 },
  },
  slideRight: {
    initial: { opacity: 0, x: -20 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: 20 },
  },
  scale: {
    initial: { opacity: 0, scale: 0.9 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 0.9 },
  },
  bounce: {
    initial: { opacity: 0, scale: 0.3 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 0.3 },
  },
}

/**
 * Transition configurations
 */
export const TRANSITIONS = {
  fast: { duration: 0.2 },
  normal: { duration: 0.3 },
  slow: { duration: 0.5 },
  spring: { type: 'spring', stiffness: 300, damping: 30 },
  bounce: { type: 'spring', stiffness: 400, damping: 10 },
}

/**
 * Glass morphism styles
 */
export const GLASS_STYLES = {
  light: 'bg-white/10 backdrop-blur-md border border-white/20',
  medium: 'bg-white/20 backdrop-blur-md border border-white/30',
  dark: 'bg-black/20 backdrop-blur-md border border-white/10',
}

/**
 * Gradient backgrounds
 */
export const GRADIENTS = {
  primary: 'bg-gradient-to-br from-blue-600 to-indigo-700',
  secondary: 'bg-gradient-to-br from-gray-800 to-gray-900',
  success: 'bg-gradient-to-br from-green-600 to-emerald-700',
  warning: 'bg-gradient-to-br from-yellow-600 to-orange-700',
  danger: 'bg-gradient-to-br from-red-600 to-pink-700',
  ocean: 'bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900',
}

/**
 * Shadow styles
 */
export const SHADOWS = {
  sm: 'shadow-sm',
  md: 'shadow-md',
  lg: 'shadow-lg',
  xl: 'shadow-xl',
  '2xl': 'shadow-2xl',
  glow: 'shadow-glow',
  'glow-red': 'shadow-glow-red',
  'glow-green': 'shadow-glow-green',
  'glow-yellow': 'shadow-glow-yellow',
}

/**
 * Border radius styles
 */
export const RADIUS = {
  none: 'rounded-none',
  sm: 'rounded-sm',
  md: 'rounded-md',
  lg: 'rounded-lg',
  xl: 'rounded-xl',
  '2xl': 'rounded-2xl',
  '3xl': 'rounded-3xl',
  full: 'rounded-full',
}

/**
 * Spacing utilities
 */
export const SPACING = {
  xs: 'p-1',
  sm: 'p-2',
  md: 'p-4',
  lg: 'p-6',
  xl: 'p-8',
  '2xl': 'p-12',
}

/**
 * Text sizes
 */
export const TEXT_SIZES = {
  xs: 'text-xs',
  sm: 'text-sm',
  base: 'text-base',
  lg: 'text-lg',
  xl: 'text-xl',
  '2xl': 'text-2xl',
  '3xl': 'text-3xl',
  '4xl': 'text-4xl',
  '5xl': 'text-5xl',
  '6xl': 'text-6xl',
}

/**
 * Font weights
 */
export const FONT_WEIGHTS = {
  light: 'font-light',
  normal: 'font-normal',
  medium: 'font-medium',
  semibold: 'font-semibold',
  bold: 'font-bold',
  extrabold: 'font-extrabold',
}
