# UI Components Specification

**Created**: 2026-01-08
**Status**: Draft
**Version**: 1.0.0

---

## Overview

This specification defines the complete UI component architecture for the Evolution of Todo Phase II web application. It provides comprehensive implementation details for all React components built with Next.js 14+ App Router, TypeScript, and Tailwind CSS.

### Purpose

- Define clear component hierarchy and composition patterns
- Establish Server Component vs Client Component decision criteria
- Specify props interfaces, states, and interactions for all components
- Provide complete implementation examples following SpecKit Plus conventions
- Ensure accessibility, performance, and maintainability standards

### Scope

This specification covers:
- **Page Components**: Server Components for routing and layout
- **Feature Components**: Client Components for task management
- **Shared UI Components**: Reusable primitives (Button, Modal, Input, etc.)
- **TypeScript Type Definitions**: Complete type safety
- **Styling Guidelines**: Tailwind CSS patterns and design tokens
- **Accessibility Requirements**: WCAG AA compliance
- **Performance Optimizations**: RSC, code splitting, SWR caching

### Cross-References

- **Business Logic**: `/mnt/d/hackathon-ii-evolution-todo/specs/phase-2-todo-web/features/task-crud.md`
- **API Contracts**: `/mnt/d/hackathon-ii-evolution-todo/specs/phase-2-todo-web/api/rest-endpoints.md`
- **Database Schema**: `/mnt/d/hackathon-ii-evolution-todo/specs/phase-2-todo-web/database/schema.md`
- **Implementation Agent**: `/mnt/d/hackathon-ii-evolution-todo/.claude/agents/nextjs-frontend-developer.md`

---

## 1. Component Architecture Overview

### 1.1 Architecture Principles

**React Server Components (RSC) by Default**

Next.js 14+ App Router uses Server Components by default. All components render on the server unless explicitly marked with `'use client'`.

**Benefits of Server Components**:
- Zero client-side JavaScript for static content
- Direct database/API access (optional BFF pattern)
- Improved SEO and initial page load
- Reduced bundle size
- Automatic code splitting

**When to Use Client Components**:
- Interactive event handlers (onClick, onChange)
- Browser APIs (window, localStorage)
- React hooks (useState, useEffect, useContext)
- Third-party libraries requiring client-side execution

### 1.2 Component Composition Hierarchy

```
TasksPage (Server Component)
├── CreateTaskForm (Client Component)
│   └── Modal (Client Component)
│       ├── Button (Shared)
│       ├── Input (Shared)
│       └── Textarea (Shared)
├── TaskFilters (Client Component)
│   └── Search Input + Filter Buttons
└── TaskList (Client Component)
    ├── TaskCard (Client Component)
    │   ├── StatusBadge
    │   ├── ActionMenu (Client Component)
    │   └── Button (Shared)
    ├── Pagination (Client Component)
    └── EmptyState (Shared)
```

### 1.3 Data Flow Patterns

**Server-to-Client Data Flow**:
1. Server Component fetches initial data (optional)
2. Passes serializable props to Client Components
3. Client Components use SWR for client-side fetching and caching

**Client-Side Data Fetching (SWR)**:
- Stale-While-Revalidate caching strategy
- Automatic revalidation on focus/reconnect
- Optimistic UI updates
- Error retry with exponential backoff

**State Management**:
- **URL State**: Search params for filters, pagination (useSearchParams)
- **Local State**: Component-specific UI state (useState)
- **Server State**: API data cached by SWR (useSWR)
- **Form State**: react-hook-form for complex forms

### 1.4 Server vs Client Component Decision Tree

```
START
  |
  Does component need interactivity? (onClick, onChange, etc.)
  ├── YES → Client Component
  └── NO
      |
      Does component use React hooks? (useState, useEffect, etc.)
      ├── YES → Client Component
      └── NO
          |
          Does component use browser APIs? (window, localStorage, etc.)
          ├── YES → Client Component
          └── NO → Server Component (default)
```

---

## 2. Page Components

### 2.1 TasksPage (Server Component)

**Purpose**: Main page for displaying user's task list with filters and creation form.

**File Path**: `apps/frontend/app/(authenticated)/tasks/page.tsx`

**Component Type**: Server Component (default in App Router)

**Why Server Component**:
- No client-side interactivity at page level
- Can fetch initial data server-side (optional)
- Better SEO and initial load performance
- Reduced JavaScript bundle size

#### Props Interface

```typescript
interface TasksPageProps {
  searchParams: {
    status?: 'all' | 'pending' | 'in_progress' | 'completed'
    search?: string
    page?: string
  }
}
```

#### Implementation

```typescript
// apps/frontend/app/(authenticated)/tasks/page.tsx
import { Suspense } from 'react'
import { Metadata } from 'next'
import { TaskList } from '@/components/TaskList'
import { CreateTaskForm } from '@/components/CreateTaskForm'
import { TaskFilters } from '@/components/TaskFilters'
import { TaskListSkeleton } from '@/components/skeletons/TaskListSkeleton'

export const metadata: Metadata = {
  title: 'My Tasks | Evolution of Todo',
  description: 'Manage your tasks efficiently',
}

export default async function TasksPage({
  searchParams,
}: TasksPageProps) {
  // Optional: Fetch initial data server-side
  // const initialData = await fetchTasksServerSide(searchParams)

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <p className="text-sm text-gray-600 mt-1">
            Organize and track your work
          </p>
        </div>
        <CreateTaskForm />
      </div>

      {/* Filters */}
      <TaskFilters
        defaultStatus={searchParams.status}
        defaultSearch={searchParams.search}
      />

      {/* Task List with Suspense for streaming */}
      <Suspense fallback={<TaskListSkeleton />}>
        <TaskList
          status={searchParams.status || 'all'}
          search={searchParams.search}
          page={Number(searchParams.page) || 1}
        />
      </Suspense>
    </div>
  )
}
```

#### Styling

- **Container**: `max-w-4xl` for optimal readability
- **Responsive**: Column layout on mobile, row on desktop
- **Spacing**: Consistent padding and margins using Tailwind's spacing scale
- **Typography**: Semantic heading hierarchy (h1 for page title)

#### Accessibility

- Semantic HTML structure with proper heading levels
- Page metadata for SEO and screen readers
- Focus management handled by child components

#### Performance

- Server Component reduces client-side JavaScript
- Suspense enables streaming and progressive rendering
- Metadata optimization for SEO

---

## 3. Feature Components

### 3.1 TaskList (Client Component)

**Purpose**: Displays paginated list of tasks with loading, error, and empty states.

**File Path**: `apps/frontend/app/components/TaskList.tsx`

**Component Type**: Client Component

**Why Client Component**:
- Uses SWR hook for data fetching
- Manages loading and error states
- Triggers revalidation on mutations

#### Props Interface

```typescript
interface TaskListProps {
  status?: 'all' | 'pending' | 'in_progress' | 'completed'
  search?: string
  page?: number
  limit?: number
}
```

#### Implementation

```typescript
'use client'

import { useTaskList } from '@/hooks/useTaskList'
import { TaskCard } from '@/components/TaskCard'
import { Pagination } from '@/components/Pagination'
import { Spinner } from '@/components/ui/Spinner'
import { EmptyState } from '@/components/ui/EmptyState'
import { AlertCircle } from 'lucide-react'

export function TaskList({
  status = 'all',
  search,
  page = 1,
  limit = 20
}: TaskListProps) {
  const { tasks, isLoading, error, pagination, mutate } = useTaskList({
    status,
    search,
    page,
    limit,
  })

  // Loading State
  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Spinner size="lg" />
        <span className="ml-3 text-gray-600">Loading tasks...</span>
      </div>
    )
  }

  // Error State
  if (error) {
    return (
      <div
        className="bg-red-50 border border-red-200 rounded-lg p-6 text-red-800"
        role="alert"
        aria-live="assertive"
      >
        <div className="flex items-start gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold mb-1">Failed to load tasks</h3>
            <p className="text-sm text-red-700">
              {error.message || 'An unexpected error occurred. Please try again.'}
            </p>
            <button
              onClick={() => mutate()}
              className="mt-3 text-sm font-medium text-red-800 hover:text-red-900 underline"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    )
  }

  // Empty State
  if (!tasks || tasks.length === 0) {
    const emptyMessages = {
      all: {
        icon: '📝',
        title: 'No tasks yet',
        description: 'Create your first task to get started',
      },
      pending: {
        icon: '✅',
        title: 'No pending tasks',
        description: 'All caught up! Create a new task or check other filters.',
      },
      in_progress: {
        icon: '🚀',
        title: 'No tasks in progress',
        description: 'Start working on a pending task to see it here.',
      },
      completed: {
        icon: '🎉',
        title: 'No completed tasks',
        description: 'Complete a task to see your progress here.',
      },
    }

    const message = search
      ? { icon: '🔍', title: 'No results found', description: `No tasks match "${search}"` }
      : emptyMessages[status as keyof typeof emptyMessages] || emptyMessages.all

    return <EmptyState {...message} />
  }

  // Success State
  return (
    <div className="space-y-4">
      {/* Task List */}
      <div className="space-y-3">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onUpdate={mutate}
            onDelete={mutate}
          />
        ))}
      </div>

      {/* Pagination */}
      {pagination && pagination.total_pages > 1 && (
        <Pagination
          currentPage={pagination.page}
          totalPages={pagination.total_pages}
          hasNext={pagination.has_next}
          hasPrev={pagination.has_prev}
        />
      )}

      {/* Results Summary */}
      <p className="text-center text-sm text-gray-500 mt-4">
        Showing {tasks.length} of {pagination?.total || 0} tasks
      </p>
    </div>
  )
}
```

#### Data Fetching Hook

```typescript
// apps/frontend/app/hooks/useTaskList.ts
'use client'

import useSWR from 'swr'
import { Task, PaginationMeta } from '@/types/task'

interface UseTaskListParams {
  status?: string
  search?: string
  page?: number
  limit?: number
}

interface TaskListResponse {
  tasks: Task[]
  pagination: PaginationMeta
}

const fetcher = async (url: string): Promise<TaskListResponse> => {
  const res = await fetch(url)
  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.message || 'Failed to fetch tasks')
  }
  return res.json()
}

export function useTaskList(params: UseTaskListParams) {
  const queryString = new URLSearchParams(
    Object.entries(params)
      .filter(([_, v]) => v != null && v !== 'all')
      .map(([k, v]) => [k, String(v)])
  ).toString()

  const { data, error, isLoading, mutate } = useSWR<TaskListResponse>(
    `/api/tasks${queryString ? `?${queryString}` : ''}`,
    fetcher,
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      dedupingInterval: 2000,
    }
  )

  return {
    tasks: data?.tasks,
    pagination: data?.pagination,
    isLoading,
    error,
    mutate,
  }
}
```

#### States

1. **Loading**: Centered spinner with text
2. **Error**: Red alert with retry button
3. **Empty**: Context-aware empty state (varies by filter/search)
4. **Success**: Task cards with pagination

#### User Interactions

- **Scroll**: Natural scrolling through task list
- **Pagination**: Navigate between pages
- **Retry**: Reload data on error

#### Accessibility

- Loading state announced via aria-live region
- Error state with role="alert" for immediate announcement
- Semantic HTML structure
- Keyboard navigation support

#### Styling

- Vertical spacing: `space-y-4` for cards, `space-y-3` for list items
- Loading centered with flexbox
- Error state: red color scheme (red-50, red-200, red-800)
- Empty state: centered with icon

#### Performance

- SWR caching reduces redundant requests
- Deduplication prevents duplicate fetches
- Revalidation on focus keeps data fresh
- Optimistic UI updates via mutate

---

### 3.2 TaskCard (Client Component)

**Purpose**: Display individual task with status toggle and quick actions.

**File Path**: `apps/frontend/app/components/TaskCard.tsx`

**Component Type**: Client Component

**Why Client Component**:
- Interactive buttons (complete, edit, delete)
- Dropdown menu state management
- Optimistic UI updates

#### Props Interface

```typescript
interface TaskCardProps {
  task: Task
  onUpdate?: () => void
  onDelete?: () => void
}

interface Task {
  id: string
  user_id: string
  title: string
  description?: string
  status: 'pending' | 'in_progress' | 'completed'
  created_at: string
  updated_at: string
}
```

#### Implementation

```typescript
'use client'

import { useState } from 'react'
import { CheckCircle, Circle, Trash2, Edit2, MoreVertical, Clock } from 'lucide-react'
import { updateTask, deleteTask } from '@/lib/api/tasks'
import { formatRelativeTime } from '@/lib/utils/date'
import { toast } from '@/lib/toast'

export function TaskCard({ task, onUpdate, onDelete }: TaskCardProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [showMenu, setShowMenu] = useState(false)

  // Toggle completion status
  const handleToggleComplete = async () => {
    setIsLoading(true)
    try {
      const newStatus = task.status === 'completed' ? 'pending' : 'completed'
      await updateTask(task.id, { status: newStatus })
      onUpdate?.()
      toast.success(
        newStatus === 'completed'
          ? 'Task marked as completed'
          : 'Task marked as incomplete'
      )
    } catch (error) {
      console.error('Failed to update task:', error)
      toast.error('Failed to update task. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  // Delete task with confirmation
  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) return

    setIsLoading(true)
    try {
      await deleteTask(task.id)
      onDelete?.()
      toast.success('Task deleted successfully')
    } catch (error) {
      console.error('Failed to delete task:', error)
      toast.error('Failed to delete task. Please try again.')
    } finally {
      setIsLoading(false)
      setShowMenu(false)
    }
  }

  // Open edit modal (to be implemented)
  const handleEdit = () => {
    setShowMenu(false)
    // TODO: Open edit modal with task data
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        {/* Completion Checkbox */}
        <button
          onClick={handleToggleComplete}
          disabled={isLoading}
          className="mt-0.5 text-gray-400 hover:text-blue-600 transition-colors disabled:opacity-50"
          aria-label={task.status === 'completed' ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {task.status === 'completed' ? (
            <CheckCircle className="w-5 h-5 text-green-600" aria-hidden="true" />
          ) : (
            <Circle className="w-5 h-5" aria-hidden="true" />
          )}
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          {/* Title */}
          <h3 className={`text-lg font-medium ${
            task.status === 'completed'
              ? 'line-through text-gray-500'
              : 'text-gray-900'
          }`}>
            {task.title}
          </h3>

          {/* Description */}
          {task.description && (
            <p className="text-sm text-gray-600 mt-1 line-clamp-2">
              {task.description}
            </p>
          )}

          {/* Metadata */}
          <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
            {/* Status Badge */}
            <span className={`px-2 py-1 rounded-full font-medium ${getStatusColor(task.status)}`}>
              {formatStatus(task.status)}
            </span>

            {/* Created Time */}
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" aria-hidden="true" />
              {formatRelativeTime(task.created_at)}
            </span>
          </div>
        </div>

        {/* Action Menu */}
        <div className="relative">
          <button
            onClick={() => setShowMenu(!showMenu)}
            className="p-1 text-gray-400 hover:text-gray-600 rounded hover:bg-gray-100 transition-colors"
            aria-label="Task actions"
            aria-expanded={showMenu}
            aria-haspopup="true"
          >
            <MoreVertical className="w-5 h-5" aria-hidden="true" />
          </button>

          {/* Dropdown Menu */}
          {showMenu && (
            <div
              className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-10"
              role="menu"
            >
              <button
                onClick={handleEdit}
                className="w-full flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-t-lg"
                role="menuitem"
              >
                <Edit2 className="w-4 h-4" aria-hidden="true" />
                Edit Task
              </button>
              <button
                onClick={handleDelete}
                disabled={isLoading}
                className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-b-lg disabled:opacity-50"
                role="menuitem"
              >
                <Trash2 className="w-4 h-4" aria-hidden="true" />
                Delete Task
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// Helper: Format status for display
function formatStatus(status: string): string {
  return status.replace('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}

// Helper: Get status badge color
function getStatusColor(status: string): string {
  switch (status) {
    case 'completed':
      return 'bg-green-100 text-green-800'
    case 'in_progress':
      return 'bg-blue-100 text-blue-800'
    case 'pending':
    default:
      return 'bg-gray-100 text-gray-800'
  }
}
```

#### States

1. **Normal**: Default card appearance
2. **Hover**: Shadow effect on hover
3. **Loading**: Disabled buttons during async operations
4. **Menu Open**: Dropdown menu visible
5. **Completed**: Title with line-through, muted colors

#### User Interactions

1. **Click Checkbox**: Toggle completion status
2. **Click Menu Button**: Open action menu
3. **Click Edit**: Open edit modal (future)
4. **Click Delete**: Confirm and delete task
5. **Click Outside Menu**: Close menu (future enhancement)

#### Accessibility

- ARIA labels for icon-only buttons
- `aria-expanded` and `aria-haspopup` for menu button
- Role attributes for menu
- Keyboard navigation support
- Focus management
- Color contrast meets WCAG AA standards

#### Styling

- **Card**: White background, border, rounded corners, hover shadow
- **Layout**: Flexbox with gap
- **Typography**: Responsive font sizes, line-through for completed
- **Colors**: Status-based color coding
- **Spacing**: Consistent padding and margins
- **Transitions**: Smooth color and shadow transitions

#### Performance

- Optimistic UI updates via callbacks
- Lazy menu rendering (only when open)
- Debounced actions to prevent double-clicks

---

### 3.3 CreateTaskForm (Client Component)

**Purpose**: Modal form for creating new tasks with validation.

**File Path**: `apps/frontend/app/components/CreateTaskForm.tsx`

**Component Type**: Client Component

**Why Client Component**:
- Form state management
- Modal open/close state
- Client-side validation with Zod

#### Props Interface

```typescript
interface CreateTaskFormProps {
  onSuccess?: () => void
}
```

#### Implementation

```typescript
'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Modal } from '@/components/ui/Modal'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Textarea } from '@/components/ui/Textarea'
import { createTask } from '@/lib/api/tasks'
import { toast } from '@/lib/toast'
import { Plus } from 'lucide-react'

// Validation Schema
const taskSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters')
    .trim(),
  description: z.string()
    .max(2000, 'Description must be less than 2000 characters')
    .optional()
    .transform(val => val?.trim() || undefined),
  status: z.enum(['pending', 'in_progress', 'completed'])
    .default('pending'),
})

type TaskFormData = z.infer<typeof taskSchema>

export function CreateTaskForm({ onSuccess }: CreateTaskFormProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: '',
      description: '',
      status: 'pending',
    },
  })

  const onSubmit = async (data: TaskFormData) => {
    setIsSubmitting(true)
    try {
      await createTask(data)
      reset()
      setIsOpen(false)
      onSuccess?.()
      toast.success('Task created successfully')
    } catch (error) {
      console.error('Failed to create task:', error)
      toast.error('Failed to create task. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleClose = () => {
    if (!isSubmitting) {
      setIsOpen(false)
      reset()
    }
  }

  return (
    <>
      {/* Trigger Button */}
      <Button
        onClick={() => setIsOpen(true)}
        variant="primary"
        size="md"
        icon={<Plus className="w-4 h-4" />}
      >
        New Task
      </Button>

      {/* Modal */}
      <Modal
        isOpen={isOpen}
        onClose={handleClose}
        title="Create New Task"
      >
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* Title Field */}
          <div>
            <label
              htmlFor="title"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Title <span className="text-red-600">*</span>
            </label>
            <Input
              id="title"
              {...register('title')}
              placeholder="Enter task title"
              error={errors.title?.message}
              autoFocus
              disabled={isSubmitting}
            />
          </div>

          {/* Description Field */}
          <div>
            <label
              htmlFor="description"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Description <span className="text-xs text-gray-500">(optional)</span>
            </label>
            <Textarea
              id="description"
              {...register('description')}
              placeholder="Enter task description"
              rows={4}
              error={errors.description?.message}
              disabled={isSubmitting}
            />
          </div>

          {/* Status Field */}
          <div>
            <label
              htmlFor="status"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Status
            </label>
            <select
              id="status"
              {...register('status')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 disabled:bg-gray-50"
              disabled={isSubmitting}
            >
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <Button
              type="button"
              onClick={handleClose}
              variant="secondary"
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              disabled={isSubmitting}
              loading={isSubmitting}
            >
              {isSubmitting ? 'Creating...' : 'Create Task'}
            </Button>
          </div>
        </form>
      </Modal>
    </>
  )
}
```

#### Validation Rules

**Title Validation**:
- **Required**: Must not be empty
- **Min Length**: 1 character (after trim)
- **Max Length**: 200 characters
- **Transformation**: Trimmed whitespace

**Description Validation**:
- **Optional**: Can be empty
- **Max Length**: 2000 characters
- **Transformation**: Trimmed whitespace, undefined if empty

**Status Validation**:
- **Enum**: Must be one of: 'pending', 'in_progress', 'completed'
- **Default**: 'pending'

#### States

1. **Closed**: Button visible, modal hidden
2. **Open**: Modal visible with form
3. **Submitting**: Form disabled, loading state
4. **Success**: Modal closes, form resets
5. **Error**: Toast notification, form remains open

#### User Interactions

1. **Click "New Task"**: Open modal
2. **Type in Fields**: Real-time validation
3. **Submit Form**: Validate and create task
4. **Click Cancel**: Close modal without saving
5. **Press Escape**: Close modal (handled by Modal component)

#### Accessibility

- Labels for all form fields
- Required fields marked with asterisk
- Error messages associated with fields
- Focus trap within modal
- Keyboard navigation (Tab, Escape)
- ARIA attributes from Modal component

#### Styling

- Modal overlay with backdrop
- Form with vertical spacing
- Input fields with focus rings
- Error states with red colors
- Loading button with spinner

#### Performance

- Form validation on client (instant feedback)
- Optimistic UI via onSuccess callback
- Form reset prevents stale data

---

### 3.4 TaskFilters (Client Component)

**Purpose**: Filter tasks by status and search by text.

**File Path**: `apps/frontend/app/components/TaskFilters.tsx`

**Component Type**: Client Component

**Why Client Component**:
- Interactive form controls
- URL manipulation with useRouter
- Debounced search input

#### Props Interface

```typescript
interface TaskFiltersProps {
  defaultStatus?: string
  defaultSearch?: string
}
```

#### Implementation

```typescript
'use client'

import { useState, useEffect, useTransition } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Search, X } from 'lucide-react'

const STATUS_OPTIONS = [
  { value: 'all', label: 'All Tasks' },
  { value: 'pending', label: 'Pending' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'completed', label: 'Completed' },
] as const

export function TaskFilters({ defaultStatus = 'all', defaultSearch = '' }: TaskFiltersProps) {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [isPending, startTransition] = useTransition()

  const [status, setStatus] = useState(defaultStatus)
  const [search, setSearch] = useState(defaultSearch)

  // Debounced search
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      updateFilters(status, search)
    }, 300)

    return () => clearTimeout(timeoutId)
  }, [search])

  const updateFilters = (newStatus: string, newSearch: string) => {
    const params = new URLSearchParams(searchParams)

    // Update status parameter
    if (newStatus && newStatus !== 'all') {
      params.set('status', newStatus)
    } else {
      params.delete('status')
    }

    // Update search parameter
    if (newSearch && newSearch.trim()) {
      params.set('search', newSearch.trim())
    } else {
      params.delete('search')
    }

    // Reset to page 1 when filters change
    params.delete('page')

    // Update URL with new filters
    startTransition(() => {
      router.push(`/tasks?${params.toString()}`)
    })
  }

  const handleStatusChange = (newStatus: string) => {
    setStatus(newStatus)
    updateFilters(newStatus, search)
  }

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value)
  }

  const handleClearSearch = () => {
    setSearch('')
    updateFilters(status, '')
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
      <div className="flex flex-col sm:flex-row gap-4">
        {/* Search Input */}
        <div className="flex-1">
          <div className="relative">
            <Search
              className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
              aria-hidden="true"
            />
            <input
              type="text"
              value={search}
              onChange={handleSearchChange}
              placeholder="Search tasks..."
              className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              aria-label="Search tasks"
            />
            {search && (
              <button
                onClick={handleClearSearch}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                aria-label="Clear search"
              >
                <X className="w-4 h-4" aria-hidden="true" />
              </button>
            )}
          </div>
        </div>

        {/* Status Filters */}
        <div className="flex gap-2" role="group" aria-label="Filter by status">
          {STATUS_OPTIONS.map((option) => (
            <button
              key={option.value}
              onClick={() => handleStatusChange(option.value)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                status === option.value
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              aria-pressed={status === option.value}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* Loading Indicator */}
      {isPending && (
        <div className="mt-2 text-sm text-gray-500">
          Updating filters...
        </div>
      )}
    </div>
  )
}
```

#### Features

**Search Input**:
- Debounced input (300ms delay)
- Clear button when search is active
- Icon for visual clarity
- Accessible label

**Status Filters**:
- Toggle buttons for each status
- Active state styling
- Aria-pressed for accessibility
- Responsive layout

**URL State Management**:
- Filters persist in URL
- Browser back/forward support
- Direct link sharing
- Page resets to 1 on filter change

#### States

1. **Default**: All filters inactive
2. **Searching**: Search input active, debounce timer running
3. **Filtered**: Active filter buttons highlighted
4. **Loading**: useTransition shows loading state

#### User Interactions

1. **Type in Search**: Debounced filter update
2. **Click Status Button**: Immediate filter update
3. **Click Clear (X)**: Clear search input
4. **Browser Back**: Restore previous filters from URL

#### Accessibility

- ARIA labels for inputs and buttons
- `aria-pressed` for toggle buttons
- Role group for filter buttons
- Keyboard navigation support

#### Styling

- Responsive layout (column on mobile, row on desktop)
- Search input with icons
- Active/inactive filter button states
- Loading indicator below filters

#### Performance

- Debounced search reduces API calls
- useTransition prevents UI blocking
- URL-based state eliminates prop drilling

---

### 3.5 Pagination (Client Component)

**Purpose**: Navigate between pages of tasks.

**File Path**: `apps/frontend/app/components/Pagination.tsx`

**Component Type**: Client Component

**Why Client Component**:
- URL manipulation with useRouter
- Interactive page navigation

#### Props Interface

```typescript
interface PaginationProps {
  currentPage: number
  totalPages: number
  hasNext: boolean
  hasPrev: boolean
}
```

#### Implementation

```typescript
'use client'

import { useRouter, useSearchParams } from 'next/navigation'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Button } from '@/components/ui/Button'

export function Pagination({
  currentPage,
  totalPages,
  hasNext,
  hasPrev
}: PaginationProps) {
  const router = useRouter()
  const searchParams = useSearchParams()

  const navigateToPage = (page: number) => {
    const params = new URLSearchParams(searchParams)
    params.set('page', String(page))
    router.push(`/tasks?${params.toString()}`)
  }

  const handlePrevious = () => {
    if (hasPrev) {
      navigateToPage(currentPage - 1)
    }
  }

  const handleNext = () => {
    if (hasNext) {
      navigateToPage(currentPage + 1)
    }
  }

  // Generate page numbers to display
  const getPageNumbers = (): (number | string)[] => {
    const pages: (number | string)[] = []
    const maxVisible = 5

    if (totalPages <= maxVisible) {
      // Show all pages
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      // Show first, last, current, and surrounding pages
      if (currentPage <= 3) {
        for (let i = 1; i <= 4; i++) pages.push(i)
        pages.push('...')
        pages.push(totalPages)
      } else if (currentPage >= totalPages - 2) {
        pages.push(1)
        pages.push('...')
        for (let i = totalPages - 3; i <= totalPages; i++) pages.push(i)
      } else {
        pages.push(1)
        pages.push('...')
        for (let i = currentPage - 1; i <= currentPage + 1; i++) pages.push(i)
        pages.push('...')
        pages.push(totalPages)
      }
    }

    return pages
  }

  if (totalPages <= 1) return null

  return (
    <nav
      className="flex items-center justify-center gap-2 mt-6"
      aria-label="Pagination navigation"
    >
      {/* Previous Button */}
      <Button
        onClick={handlePrevious}
        disabled={!hasPrev}
        variant="secondary"
        size="sm"
        icon={<ChevronLeft className="w-4 h-4" />}
        aria-label="Previous page"
      >
        Previous
      </Button>

      {/* Page Numbers */}
      <div className="flex items-center gap-1">
        {getPageNumbers().map((page, index) => (
          typeof page === 'number' ? (
            <button
              key={index}
              onClick={() => navigateToPage(page)}
              className={`min-w-[2.5rem] h-10 px-3 rounded-md text-sm font-medium transition-colors ${
                page === currentPage
                  ? 'bg-blue-600 text-white'
                  : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
              }`}
              aria-label={`Page ${page}`}
              aria-current={page === currentPage ? 'page' : undefined}
            >
              {page}
            </button>
          ) : (
            <span
              key={index}
              className="px-2 text-gray-500"
              aria-hidden="true"
            >
              {page}
            </span>
          )
        ))}
      </div>

      {/* Next Button */}
      <Button
        onClick={handleNext}
        disabled={!hasNext}
        variant="secondary"
        size="sm"
        icon={<ChevronRight className="w-4 h-4" />}
        iconPosition="right"
        aria-label="Next page"
      >
        Next
      </Button>
    </nav>
  )
}
```

#### Features

- Smart page number display (max 5 visible)
- Ellipsis for large page ranges
- Previous/Next buttons with disabled states
- Current page highlighted
- URL-based navigation

#### User Interactions

1. **Click Page Number**: Navigate to specific page
2. **Click Previous**: Go to previous page
3. **Click Next**: Go to next page
4. **Disabled State**: Buttons disabled at boundaries

#### Accessibility

- Navigation landmark with aria-label
- aria-current for current page
- aria-label for page buttons
- Disabled state properly indicated

#### Styling

- Centered flexbox layout
- Button styles (primary for current, secondary for others)
- Responsive spacing
- Hover states

---

## 4. Shared UI Components

### 4.1 Modal

**Purpose**: Reusable modal dialog with overlay and focus trap.

**File Path**: `apps/frontend/app/components/ui/Modal.tsx`

**Implementation**:

```typescript
'use client'

import { useEffect, useRef, Fragment } from 'react'
import { createPortal } from 'react-dom'
import { X } from 'lucide-react'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const overlayRef = useRef<HTMLDivElement>(null)
  const modalRef = useRef<HTMLDivElement>(null)

  // Focus trap and escape key handler
  useEffect(() => {
    if (!isOpen) return

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }

    const focusableElements = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    const firstElement = focusableElements?.[0] as HTMLElement
    const lastElement = focusableElements?.[focusableElements.length - 1] as HTMLElement

    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return

      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault()
        lastElement?.focus()
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault()
        firstElement?.focus()
      }
    }

    document.addEventListener('keydown', handleEscape)
    document.addEventListener('keydown', handleTab)
    firstElement?.focus()

    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.removeEventListener('keydown', handleTab)
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  return createPortal(
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        ref={overlayRef}
        className="absolute inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal */}
      <div
        ref={modalRef}
        className="relative bg-white rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 id="modal-title" className="text-xl font-semibold text-gray-900">
            {title}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" aria-hidden="true" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {children}
        </div>
      </div>
    </div>,
    document.body
  )
}
```

**Features**:
- Portal rendering (outside React tree)
- Focus trap (Tab/Shift+Tab)
- Escape key to close
- Backdrop click to close
- Scrollable content
- Accessible (ARIA attributes)

---

### 4.2 Button

**Purpose**: Reusable button component with variants and states.

**File Path**: `apps/frontend/app/components/ui/Button.tsx`

**Implementation**:

```typescript
'use client'

import { forwardRef } from 'react'
import { Spinner } from './Spinner'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  icon?: React.ReactNode
  iconPosition?: 'left' | 'right'
  children?: React.ReactNode
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({
    variant = 'primary',
    size = 'md',
    loading = false,
    icon,
    iconPosition = 'left',
    disabled,
    className = '',
    children,
    ...props
  }, ref) => {
    const baseStyles = 'inline-flex items-center justify-center font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'

    const variantStyles = {
      primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
      secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200 focus:ring-gray-500',
      danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
    }

    const sizeStyles = {
      sm: 'px-3 py-1.5 text-sm gap-1.5',
      md: 'px-4 py-2 text-base gap-2',
      lg: 'px-6 py-3 text-lg gap-2.5',
    }

    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
        {...props}
      >
        {loading && <Spinner size="sm" />}
        {!loading && icon && iconPosition === 'left' && icon}
        {children}
        {!loading && icon && iconPosition === 'right' && icon}
      </button>
    )
  }
)

Button.displayName = 'Button'
```

---

### 4.3 Input

**Purpose**: Text input with error states.

**File Path**: `apps/frontend/app/components/ui/Input.tsx`

**Implementation**:

```typescript
'use client'

import { forwardRef } from 'react'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ error, className = '', ...props }, ref) => {
    return (
      <div>
        <input
          ref={ref}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 transition-colors disabled:opacity-50 disabled:bg-gray-50 ${
            error
              ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
              : 'border-gray-300 focus:ring-blue-500 focus:border-transparent'
          } ${className}`}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? `${props.id}-error` : undefined}
          {...props}
        />
        {error && (
          <p
            id={`${props.id}-error`}
            className="mt-1 text-sm text-red-600"
            role="alert"
          >
            {error}
          </p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'
```

---

### 4.4 Textarea

**Purpose**: Multi-line text input with error states.

**File Path**: `apps/frontend/app/components/ui/Textarea.tsx`

**Implementation**:

```typescript
'use client'

import { forwardRef } from 'react'

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  error?: string
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ error, className = '', ...props }, ref) => {
    return (
      <div>
        <textarea
          ref={ref}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 transition-colors resize-vertical disabled:opacity-50 disabled:bg-gray-50 ${
            error
              ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
              : 'border-gray-300 focus:ring-blue-500 focus:border-transparent'
          } ${className}`}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? `${props.id}-error` : undefined}
          {...props}
        />
        {error && (
          <p
            id={`${props.id}-error`}
            className="mt-1 text-sm text-red-600"
            role="alert"
          >
            {error}
          </p>
        )}
      </div>
    )
  }
)

Textarea.displayName = 'Textarea'
```

---

### 4.5 Spinner

**Purpose**: Loading indicator.

**File Path**: `apps/frontend/app/components/ui/Spinner.tsx`

**Implementation**:

```typescript
'use client'

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function Spinner({ size = 'md', className = '' }: SpinnerProps) {
  const sizeStyles = {
    sm: 'w-4 h-4 border-2',
    md: 'w-6 h-6 border-2',
    lg: 'w-8 h-8 border-3',
  }

  return (
    <div
      className={`animate-spin rounded-full border-t-transparent border-current ${sizeStyles[size]} ${className}`}
      role="status"
      aria-label="Loading"
    >
      <span className="sr-only">Loading...</span>
    </div>
  )
}
```

---

### 4.6 EmptyState

**Purpose**: Display message when no data is available.

**File Path**: `apps/frontend/app/components/ui/EmptyState.tsx`

**Implementation**:

```typescript
'use client'

interface EmptyStateProps {
  icon: string
  title: string
  description: string
}

export function EmptyState({ icon, title, description }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <div className="text-6xl mb-4" role="img" aria-label={icon}>
        {icon}
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        {title}
      </h3>
      <p className="text-sm text-gray-600 max-w-md">
        {description}
      </p>
    </div>
  )
}
```

---

## 5. TypeScript Type Definitions

**File Path**: `apps/frontend/app/types/task.ts`

```typescript
// Task Entity
export interface Task {
  id: string
  user_id: string
  title: string
  description?: string
  status: TaskStatus
  created_at: string
  updated_at: string
}

// Task Status Enum
export type TaskStatus = 'pending' | 'in_progress' | 'completed'

// Task Creation Payload
export interface TaskCreate {
  title: string
  description?: string
  status?: TaskStatus
}

// Task Update Payload
export interface TaskUpdate {
  title?: string
  description?: string
  status?: TaskStatus
}

// Pagination Metadata
export interface PaginationMeta {
  page: number
  limit: number
  total: number
  total_pages: number
  has_next: boolean
  has_prev: boolean
}

// Task List API Response
export interface TaskListResponse {
  tasks: Task[]
  pagination: PaginationMeta
}

// Task Detail API Response
export interface TaskDetailResponse {
  task: Task
}

// API Error Response
export interface APIError {
  error: string
  message: string
  status_code: number
}
```

---

## 6. Styling Guidelines

### 6.1 Design Tokens

**Color Palette**:
```typescript
const colors = {
  primary: {
    50: '#eff6ff',
    100: '#dbeafe',
    // ... (Tailwind blue scale)
    600: '#2563eb', // Primary blue
    700: '#1d4ed8',
  },
  gray: {
    // ... (Tailwind gray scale)
    100: '#f3f4f6',
    600: '#4b5563',
  },
  green: {
    // Success colors
    600: '#16a34a',
  },
  red: {
    // Error/danger colors
    600: '#dc2626',
  },
}
```

**Typography**:
- Font Family: System font stack (`font-sans`)
- Sizes: `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, etc.
- Weights: `font-normal`, `font-medium`, `font-semibold`, `font-bold`

**Spacing**:
- Based on 4px grid: `space-1` (0.25rem), `space-2` (0.5rem), etc.
- Common gaps: `gap-2`, `gap-3`, `gap-4`
- Padding: `p-4`, `px-6`, `py-3`

**Border Radius**:
- Small: `rounded` (0.25rem)
- Medium: `rounded-md` (0.375rem)
- Large: `rounded-lg` (0.5rem)
- Full: `rounded-full` (9999px)

### 6.2 Responsive Design

**Breakpoints**:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

**Mobile-First Approach**:
```tsx
// Default styles for mobile
<div className="flex-col">
  {/* Stack vertically on mobile */}
</div>

// Override for desktop
<div className="flex-col sm:flex-row">
  {/* Stack horizontally on tablet+ */}
</div>
```

### 6.3 Dark Mode (Future)

Currently not implemented, but structure supports it:
```tsx
<div className="bg-white dark:bg-gray-800">
  {/* Light mode: white, Dark mode: gray-800 */}
</div>
```

---

## 7. Accessibility Requirements

### 7.1 WCAG AA Compliance

**Color Contrast**:
- Text: 4.5:1 ratio minimum
- Large text: 3:1 ratio minimum
- UI components: 3:1 ratio minimum

**Keyboard Navigation**:
- All interactive elements accessible via Tab
- Focus indicators visible (ring-2 ring-blue-500)
- Logical tab order
- Escape key closes modals

**Screen Reader Support**:
- Semantic HTML elements
- ARIA labels for icon-only buttons
- ARIA live regions for dynamic content
- Role attributes for custom widgets

### 7.2 Implementation Checklist

- [x] Semantic HTML (header, nav, main, button, etc.)
- [x] ARIA labels for icons
- [x] Focus management in modals
- [x] Keyboard shortcuts (Escape)
- [x] Error messages announced
- [x] Loading states announced
- [x] Form validation messages associated with inputs
- [x] Color contrast meets WCAG AA
- [ ] Skip to main content link (future)
- [ ] Landmark regions (future enhancement)

---

## 8. Performance Considerations

### 8.1 Server Components Strategy

**Default to Server Components**:
- Reduces client-side JavaScript bundle
- Faster initial page load
- Better SEO

**Client Components Only When Needed**:
- Interactive features (forms, buttons)
- Browser APIs (localStorage, window)
- React hooks (useState, useEffect)

### 8.2 Code Splitting

**Automatic Splitting**:
- Next.js automatically splits by route
- Each page is a separate bundle

**Dynamic Imports** (Future):
```tsx
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Spinner />,
})
```

### 8.3 Data Fetching

**SWR Caching**:
- Deduplicate requests (2 second window)
- Revalidate on focus
- Revalidate on reconnect
- Stale-while-revalidate strategy

**Optimistic Updates**:
```typescript
// Optimistically update UI before API call
mutate(
  updatedData,
  { optimisticData: updatedData, rollbackOnError: true }
)
```

### 8.4 Image Optimization

Use `next/image` for all images:
```tsx
import Image from 'next/image'

<Image
  src="/task-icon.png"
  alt="Task icon"
  width={24}
  height={24}
  priority={false}
/>
```

---

## 9. Testing Strategy

### 9.1 Unit Testing (Jest + React Testing Library)

**Test File Location**: `apps/frontend/app/components/__tests__/TaskCard.test.tsx`

**Example Test**:
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { TaskCard } from '../TaskCard'

describe('TaskCard', () => {
  const mockTask = {
    id: '1',
    user_id: 'user-1',
    title: 'Test Task',
    description: 'Test description',
    status: 'pending' as const,
    created_at: '2026-01-08T00:00:00Z',
    updated_at: '2026-01-08T00:00:00Z',
  }

  it('renders task title and description', () => {
    render(<TaskCard task={mockTask} />)
    expect(screen.getByText('Test Task')).toBeInTheDocument()
    expect(screen.getByText('Test description')).toBeInTheDocument()
  })

  it('toggles completion status on checkbox click', async () => {
    const mockOnUpdate = jest.fn()
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} />)

    const checkbox = screen.getByLabelText('Mark as complete')
    fireEvent.click(checkbox)

    await waitFor(() => {
      expect(mockOnUpdate).toHaveBeenCalled()
    })
  })
})
```

### 9.2 E2E Testing (Playwright)

**Test File Location**: `apps/frontend/tests/e2e/tasks.spec.ts`

**Example Test**:
```typescript
import { test, expect } from '@playwright/test'

test.describe('Task Management', () => {
  test('creates a new task', async ({ page }) => {
    await page.goto('/tasks')

    // Click "New Task" button
    await page.click('text=New Task')

    // Fill form
    await page.fill('#title', 'E2E Test Task')
    await page.fill('#description', 'Created by Playwright')

    // Submit
    await page.click('text=Create Task')

    // Verify task appears
    await expect(page.locator('text=E2E Test Task')).toBeVisible()
  })
})
```

---

## 10. Implementation Notes

### 10.1 API Client Library

**File Path**: `apps/frontend/app/lib/api/tasks.ts`

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function createTask(data: TaskCreate): Promise<Task> {
  const res = await fetch(`${API_BASE_URL}/api/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getAuthToken()}`,
    },
    body: JSON.stringify(data),
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.message || 'Failed to create task')
  }

  const result = await res.json()
  return result.task
}

export async function updateTask(id: string, data: TaskUpdate): Promise<Task> {
  const res = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getAuthToken()}`,
    },
    body: JSON.stringify(data),
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.message || 'Failed to update task')
  }

  const result = await res.json()
  return result.task
}

export async function deleteTask(id: string): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${getAuthToken()}`,
    },
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.message || 'Failed to delete task')
  }
}

function getAuthToken(): string {
  // TODO: Implement authentication
  return ''
}
```

### 10.2 Utility Functions

**Date Formatting** (`apps/frontend/app/lib/utils/date.ts`):
```typescript
export function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000)

  if (diffInSeconds < 60) return 'just now'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`

  return date.toLocaleDateString()
}
```

**Toast Notifications** (`apps/frontend/app/lib/toast.ts`):
```typescript
// Simple toast implementation (or use react-hot-toast)
export const toast = {
  success: (message: string) => {
    // Implementation
  },
  error: (message: string) => {
    // Implementation
  },
}
```

---

## 11. Cross-References

### 11.1 Related Specifications

- **Feature Spec**: `/mnt/d/hackathon-ii-evolution-todo/specs/phase-2-todo-web/features/task-crud.md` (business logic)
- **API Spec**: `/mnt/d/hackathon-ii-evolution-todo/specs/phase-2-todo-web/api/rest-endpoints.md` (API contracts)
- **Database Spec**: `/mnt/d/hackathon-ii-evolution-todo/specs/phase-2-todo-web/database/schema.md` (data model)

### 11.2 Implementation Resources

- **Frontend Agent**: `/mnt/d/hackathon-ii-evolution-todo/.claude/agents/nextjs-frontend-developer.md`
- **Next.js Docs**: https://nextjs.org/docs
- **Tailwind Docs**: https://tailwindcss.com/docs
- **SWR Docs**: https://swr.vercel.app

### 11.3 Design Assets

- **Component Wireframes**: TBD
- **Design System**: TBD
- **Brand Guidelines**: TBD

---

## 12. Changelog

### Version 1.0.0 (2026-01-08)
- Initial specification created
- Defined all core components
- Established architecture patterns
- Added complete implementation examples

---

## 13. Next Steps

1. **Review and Approve**: Validate spec with stakeholders
2. **Create Architecture Plan**: Run `/sp.plan` to generate technical design
3. **Break Down Tasks**: Run `/sp.tasks` to create implementation tasks
4. **Implement Components**: Use `nextjs-frontend-developer` agent
5. **Write Tests**: Unit tests + E2E tests
6. **Documentation**: Add Storybook or component documentation

---

**Specification Author**: Claude Sonnet 4.5 (Specification Architect Agent)
**Date Created**: 2026-01-08
**SpecKit Plus Version**: 1.0
**Status**: Draft - Awaiting Review
