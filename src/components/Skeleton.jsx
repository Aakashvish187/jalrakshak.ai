import React from 'react'

/**
 * Skeleton loading component
 */
export function Skeleton({ className = '', ...props }) {
  return (
    <div
      className={`animate-pulse bg-gray-700 rounded ${className}`}
      {...props}
    />
  )
}

/**
 * Card skeleton
 */
export function CardSkeleton() {
  return (
    <div className="glass-card p-6">
      <div className="flex items-center space-x-4">
        <Skeleton className="h-12 w-12 rounded-full" />
        <div className="space-y-2 flex-1">
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-4 w-1/2" />
        </div>
      </div>
      <div className="mt-4 space-y-2">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
      </div>
    </div>
  )
}

/**
 * Stat card skeleton
 */
export function StatCardSkeleton() {
  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <Skeleton className="h-4 w-20" />
          <Skeleton className="h-8 w-16" />
        </div>
        <Skeleton className="h-8 w-8 rounded" />
      </div>
    </div>
  )
}

/**
 * Alert item skeleton
 */
export function AlertItemSkeleton() {
  return (
    <div className="flex items-center space-x-4 p-4 border-b border-gray-700/50">
      <Skeleton className="h-6 w-16 rounded-full" />
      <div className="flex-1 space-y-2">
        <Skeleton className="h-4 w-32" />
        <Skeleton className="h-3 w-24" />
      </div>
      <Skeleton className="h-4 w-20" />
    </div>
  )
}

/**
 * Map skeleton
 */
export function MapSkeleton() {
  return (
    <div className="glass-card p-6 h-96">
      <div className="h-full bg-gray-800 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <Skeleton className="h-8 w-8 rounded-full mx-auto mb-4" />
          <Skeleton className="h-4 w-32 mx-auto" />
        </div>
      </div>
    </div>
  )
}

/**
 * Table skeleton
 */
export function TableSkeleton({ rows = 5, columns = 4 }) {
  return (
    <div className="glass-card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-700">
          <thead className="bg-gray-800/50">
            <tr>
              {Array.from({ length: columns }).map((_, i) => (
                <th key={i} className="px-6 py-3 text-left">
                  <Skeleton className="h-4 w-20" />
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700/50">
            {Array.from({ length: rows }).map((_, i) => (
              <tr key={i}>
                {Array.from({ length: columns }).map((_, j) => (
                  <td key={j} className="px-6 py-4">
                    <Skeleton className="h-4 w-16" />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

/**
 * List skeleton
 */
export function ListSkeleton({ items = 5 }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: items }).map((_, i) => (
        <div key={i} className="glass-card p-4">
          <div className="flex items-center space-x-4">
            <Skeleton className="h-10 w-10 rounded-full" />
            <div className="flex-1 space-y-2">
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-3 w-1/2" />
            </div>
            <Skeleton className="h-6 w-16 rounded-full" />
          </div>
        </div>
      ))}
    </div>
  )
}
