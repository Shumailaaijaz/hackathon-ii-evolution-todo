# API Specification: REST Endpoints

**Version**: 1.0
**Last Updated**: 2026-01-08
**Status**: Draft

---

## Table of Contents

1. [API Overview](#1-api-overview)
2. [Authentication](#2-authentication)
3. [Task Endpoints](#3-task-endpoints)
4. [Error Response Format](#4-error-response-format)
5. [HTTP Status Codes](#5-http-status-codes)
6. [Design Decisions](#6-design-decisions)
7. [Cross-References](#7-cross-references)
8. [OpenAPI Documentation](#8-openapi-documentation)

---

## 1. API Overview

### Base URLs

**Development**:
```
http://localhost:8000
```

**Production**:
```
https://api.evolution-todo.railway.app
```

### API Versioning

- **Current Version**: v1
- **Versioning Strategy**: URL path versioning (`/api/v1/...`)
- **Future Compatibility**: v2 endpoints will coexist with v1 during transition periods
- **Deprecation Policy**: Minimum 6 months notice before removing deprecated endpoints

### Global Headers

**Request Headers**:
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
Accept: application/json
```

**Response Headers**:
```
Content-Type: application/json
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704984000
```

### CORS Configuration

**Allowed Origins**:
- Development: `http://localhost:3000`
- Production: `https://evolution-todo.vercel.app`

**Allowed Methods**: `GET, POST, PUT, PATCH, DELETE, OPTIONS`

**Allowed Headers**: `Authorization, Content-Type, Accept`

**Max Age**: 3600 seconds (1 hour)

### Rate Limiting

- **Limit**: 100 requests per minute per user
- **Window**: Sliding window of 60 seconds
- **Response**: 429 Too Many Requests when exceeded
- **Headers**: `X-RateLimit-*` headers in all responses

---

## 2. Authentication

### Authentication Mechanism

All API endpoints require **JWT (JSON Web Token)** authentication.

### Header Format

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Structure

JWT payload contains:
```json
{
  "sub": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "exp": 1704984000,
  "iat": 1704897600
}
```

- `sub`: User ID (UUID)
- `email`: User's email address
- `exp`: Token expiration timestamp (Unix time)
- `iat`: Token issued at timestamp (Unix time)

### Token Lifecycle

- **Expiration**: 24 hours from issuance
- **Refresh**: Use refresh token to obtain new access token
- **Revocation**: Logout invalidates refresh token

### Authentication Errors

**401 Unauthorized** - Missing or invalid token:
```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid authentication token",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

**403 Forbidden** - Valid token but insufficient permissions:
```json
{
  "error": "Forbidden",
  "message": "You do not have permission to access this resource",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

### Cross-Reference

For complete authentication flow (login, signup, token refresh), see:
- **specs/features/authentication.md** (business logic)
- **specs/api/auth-endpoints.md** (auth API endpoints)

---

## 3. Task Endpoints

### 3.1 GET /api/tasks

**Purpose**: Retrieve all tasks for the authenticated user

#### Request

**Method**: `GET`

**URL**: `/api/tasks`

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Query Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | string | No | `all` | Filter by status: `pending`, `in_progress`, `completed`, or `all` |
| `page` | integer | No | `1` | Page number (1-indexed) |
| `limit` | integer | No | `20` | Results per page (max 100) |
| `sort` | string | No | `created_at` | Sort field: `created_at`, `updated_at`, or `title` |
| `order` | string | No | `desc` | Sort order: `asc` or `desc` |
| `search` | string | No | - | Search query (searches title and description) |

**Example Request**:
```http
GET /api/tasks?status=pending&page=1&limit=10&sort=created_at&order=desc HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
```

#### Response 200 OK

**Success Response**:
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread, butter, cheese",
      "status": "pending",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "user_id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Call dentist",
      "description": "Schedule annual checkup appointment",
      "status": "pending",
      "created_at": "2024-01-14T15:20:00Z",
      "updated_at": "2024-01-14T15:20:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 45,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

**Response Schema**:
```typescript
interface GetTasksResponse {
  tasks: Task[];
  pagination: PaginationMetadata;
}

interface Task {
  id: string;                    // UUID
  user_id: string;               // UUID (from JWT, not URL)
  title: string;                 // 1-200 characters
  description: string | null;    // 0-2000 characters
  status: "pending" | "in_progress" | "completed";
  created_at: string;            // ISO 8601 datetime
  updated_at: string;            // ISO 8601 datetime
}

interface PaginationMetadata {
  page: number;                  // Current page (1-indexed)
  limit: number;                 // Results per page
  total: number;                 // Total number of tasks
  total_pages: number;           // Total number of pages
  has_next: boolean;             // Has next page
  has_prev: boolean;             // Has previous page
}
```

#### Error Responses

**401 Unauthorized** - Missing or invalid JWT:
```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid authentication token",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

**400 Bad Request** - Invalid query parameters:
```json
{
  "error": "Bad Request",
  "message": "Invalid query parameters",
  "details": [
    {
      "field": "limit",
      "message": "limit must be between 1 and 100"
    },
    {
      "field": "status",
      "message": "status must be one of: pending, in_progress, completed, all"
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

#### Implementation Notes

1. **User Isolation**: Tasks are automatically filtered by `user_id` extracted from JWT
2. **Performance**: Add database index on `(user_id, status, created_at)` for efficient filtering
3. **Search**: Implement case-insensitive full-text search on `title` and `description`
4. **Default Ordering**: Most recently created tasks first
5. **Empty Results**: Return empty array with valid pagination metadata

---

### 3.2 POST /api/tasks

**Purpose**: Create a new task for the authenticated user

#### Request

**Method**: `POST`

**URL**: `/api/tasks`

**Headers**:
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, butter, cheese",
  "status": "pending"
}
```

**Request Schema**:
```typescript
interface CreateTaskRequest {
  title: string;                 // Required, 1-200 characters
  description?: string | null;   // Optional, 0-2000 characters
  status?: "pending" | "in_progress" | "completed";  // Optional, default: "pending"
}
```

**Validation Rules**:
- `title`: Required, trimmed, 1-200 characters after trimming
- `description`: Optional, 0-2000 characters, can be null or empty string
- `status`: Optional, must be one of: `pending`, `in_progress`, `completed`
- `user_id`: Automatically extracted from JWT (NOT in request body)

**Example Request**:
```http
POST /api/tasks HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, butter, cheese",
  "status": "pending"
}
```

#### Response 201 Created

**Success Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, butter, cheese",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Response Schema**:
```typescript
interface CreateTaskResponse extends Task {
  // Same as Task interface
}
```

#### Error Responses

**401 Unauthorized** - Missing or invalid JWT:
```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid authentication token",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

**400 Bad Request** - Validation errors:
```json
{
  "error": "Validation Error",
  "message": "Request validation failed",
  "details": [
    {
      "field": "title",
      "message": "Title is required and must be 1-200 characters"
    },
    {
      "field": "description",
      "message": "Description must not exceed 2000 characters"
    },
    {
      "field": "status",
      "message": "Status must be one of: pending, in_progress, completed"
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

**422 Unprocessable Entity** - Invalid JSON or schema mismatch:
```json
{
  "error": "Unprocessable Entity",
  "message": "Invalid JSON payload",
  "details": [
    {
      "field": "body",
      "message": "Expected JSON object with 'title' field"
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

#### Implementation Notes

1. **Auto-Generated Fields**:
   - `id`: Generated as UUID v4
   - `user_id`: Extracted from JWT token (sub claim)
   - `created_at`: Set to current UTC timestamp
   - `updated_at`: Set to current UTC timestamp

2. **Input Sanitization**:
   - Trim whitespace from `title`
   - Trim whitespace from `description`
   - Reject empty title after trimming

3. **Database Transaction**: Use transaction to ensure atomic creation

4. **Response Headers**:
   - `Location: /api/tasks/{id}` - URL of created resource

---

### 3.3 GET /api/tasks/{id}

**Purpose**: Retrieve a single task by ID for the authenticated user

#### Request

**Method**: `GET`

**URL**: `/api/tasks/{id}`

**Path Parameters**:
- `id`: Task UUID (e.g., `550e8400-e29b-41d4-a716-446655440000`)

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Example Request**:
```http
GET /api/tasks/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
```

#### Response 200 OK

**Success Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, butter, cheese",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Response Schema**:
```typescript
interface GetTaskResponse extends Task {
  // Same as Task interface
}
```

#### Error Responses

**401 Unauthorized** - Missing or invalid JWT:
```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid authentication token",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

**400 Bad Request** - Invalid UUID format:
```json
{
  "error": "Bad Request",
  "message": "Invalid task ID format",
  "details": [
    {
      "field": "id",
      "message": "Task ID must be a valid UUID"
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks/invalid-uuid"
}
```

**404 Not Found** - Task doesn't exist or belongs to different user:
```json
{
  "error": "Not Found",
  "message": "Task not found",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

#### Implementation Notes

1. **User Isolation**: Query must filter by BOTH `id` AND `user_id` from JWT
2. **404 vs 403**: Return 404 for both "doesn't exist" and "belongs to other user" to avoid information leakage
3. **UUID Validation**: Validate UUID format before database query
4. **Performance**: Database index on `(id, user_id)` for efficient lookup

---

### 3.4 PUT /api/tasks/{id}

**Purpose**: Update a task (full replacement) for the authenticated user

#### Request

**Method**: `PUT`

**URL**: `/api/tasks/{id}`

**Path Parameters**:
- `id`: Task UUID

**Headers**:
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken, vegetables",
  "status": "in_progress"
}
```

**Request Schema**:
```typescript
interface UpdateTaskRequest {
  title: string;                 // Required, 1-200 characters
  description?: string | null;   // Optional, 0-2000 characters
  status: "pending" | "in_progress" | "completed";  // Required
}
```

**Validation Rules**: Same as POST /api/tasks

**Example Request**:
```http
PUT /api/tasks/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken, vegetables",
  "status": "in_progress"
}
```

#### Response 200 OK

**Success Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken, vegetables",
  "status": "in_progress",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T14:25:00Z"
}
```

**Response Schema**:
```typescript
interface UpdateTaskResponse extends Task {
  // Same as Task interface
}
```

#### Error Responses

**401 Unauthorized** - Missing or invalid JWT:
```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid authentication token",
  "details": null,
  "timestamp": "2024-01-15T14:25:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

**403 Forbidden** - Task belongs to different user:
```json
{
  "error": "Forbidden",
  "message": "You do not have permission to update this task",
  "details": null,
  "timestamp": "2024-01-15T14:25:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

**404 Not Found** - Task doesn't exist:
```json
{
  "error": "Not Found",
  "message": "Task not found",
  "details": null,
  "timestamp": "2024-01-15T14:25:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

**400 Bad Request** - Validation errors:
```json
{
  "error": "Validation Error",
  "message": "Request validation failed",
  "details": [
    {
      "field": "title",
      "message": "Title is required and must be 1-200 characters"
    }
  ],
  "timestamp": "2024-01-15T14:25:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "details": null,
  "timestamp": "2024-01-15T14:25:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

#### Implementation Notes

1. **Full Replacement**: PUT replaces ALL fields (title, description, status)
2. **Partial Updates**: Use PATCH for partial updates (see 3.5)
3. **Immutable Fields**: `id`, `user_id`, `created_at` cannot be changed
4. **Updated Timestamp**: `updated_at` automatically set to current UTC timestamp
5. **Optimistic Locking**: Consider adding `version` field for concurrent update handling
6. **User Isolation**: Verify `user_id` from JWT matches task owner before update

---

### 3.5 PATCH /api/tasks/{id}

**Purpose**: Partially update a task for the authenticated user

#### Request

**Method**: `PATCH`

**URL**: `/api/tasks/{id}`

**Path Parameters**:
- `id`: Task UUID

**Headers**:
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body** (all fields optional):
```json
{
  "status": "completed"
}
```

**Request Schema**:
```typescript
interface PartialUpdateTaskRequest {
  title?: string;                // Optional, 1-200 characters if provided
  description?: string | null;   // Optional, 0-2000 characters if provided
  status?: "pending" | "in_progress" | "completed";  // Optional
}
```

**Validation Rules**:
- All fields optional
- If provided, must meet same validation as PUT
- At least one field must be provided

**Example Requests**:

Update status only:
```http
PATCH /api/tasks/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "status": "completed"
}
```

Update title and description:
```http
PATCH /api/tasks/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries (updated)",
  "description": "Added organic vegetables to the list"
}
```

#### Response 200 OK

**Success Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, butter, cheese",
  "status": "completed",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T16:45:00Z"
}
```

**Response Schema**:
```typescript
interface PartialUpdateTaskResponse extends Task {
  // Same as Task interface - returns full task
}
```

#### Error Responses

Same as PUT /api/tasks/{id}, plus:

**400 Bad Request** - No fields provided:
```json
{
  "error": "Bad Request",
  "message": "At least one field must be provided for update",
  "details": null,
  "timestamp": "2024-01-15T16:45:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

#### Implementation Notes

1. **Partial Update**: Only provided fields are updated
2. **Unchanged Fields**: Non-provided fields retain current values
3. **Updated Timestamp**: `updated_at` always set to current UTC timestamp
4. **Return Full Object**: Response contains complete updated task
5. **Empty Object**: Reject PATCH with empty body `{}`

---

### 3.6 PATCH /api/tasks/{id}/complete

**Purpose**: Mark a task as completed (convenience endpoint)

#### Request

**Method**: `PATCH`

**URL**: `/api/tasks/{id}/complete`

**Path Parameters**:
- `id`: Task UUID

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Request Body**: Empty or `{}`

**Example Request**:
```http
PATCH /api/tasks/550e8400-e29b-41d4-a716-446655440000/complete HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Response 200 OK

**Success Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, butter, cheese",
  "status": "completed",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T16:45:00Z"
}
```

**Response Schema**:
```typescript
interface CompleteTaskResponse extends Task {
  // Same as Task interface with status: "completed"
}
```

#### Error Responses

Same as PATCH /api/tasks/{id}

#### Implementation Notes

1. **Idempotent**: Marking completed task as completed is safe (no error)
2. **Convenience**: Equivalent to `PATCH /api/tasks/{id}` with `{"status": "completed"}`
3. **Alternative Endpoint**: Consider `PATCH /api/tasks/{id}/uncomplete` for reverting
4. **Updated Timestamp**: `updated_at` set to current UTC timestamp even if already completed

---

### 3.7 DELETE /api/tasks/{id}

**Purpose**: Permanently delete a task for the authenticated user

#### Request

**Method**: `DELETE`

**URL**: `/api/tasks/{id}`

**Path Parameters**:
- `id`: Task UUID

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Example Request**:
```http
DELETE /api/tasks/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Response 204 No Content

**Success Response**:
- **Status Code**: 204
- **Body**: Empty (no content)
- **Headers**: Standard response headers only

#### Error Responses

**401 Unauthorized** - Missing or invalid JWT:
```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid authentication token",
  "details": null,
  "timestamp": "2024-01-15T17:00:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

**403 Forbidden** - Task belongs to different user:
```json
{
  "error": "Forbidden",
  "message": "You do not have permission to delete this task",
  "details": null,
  "timestamp": "2024-01-15T17:00:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

**404 Not Found** - Task doesn't exist:
```json
{
  "error": "Not Found",
  "message": "Task not found",
  "details": null,
  "timestamp": "2024-01-15T17:00:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "details": null,
  "timestamp": "2024-01-15T17:00:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

#### Implementation Notes

1. **Hard Delete**: Task permanently removed from database (no soft delete)
2. **Idempotent**: Deleting non-existent task returns 404 (not 204)
3. **User Isolation**: Verify `user_id` from JWT matches task owner before deletion
4. **Cascading**: Consider future relations (tags, attachments) for cascade rules
5. **Audit Trail**: Consider logging deletions for compliance/recovery

---

## 4. Error Response Format

All API error responses follow a consistent structure.

### Standard Error Schema

```typescript
interface ErrorResponse {
  error: string;                 // Error type/category
  message: string;               // Human-readable error message
  details: ErrorDetail[] | null; // Detailed validation errors (optional)
  timestamp: string;             // ISO 8601 datetime of error
  path: string;                  // Request path that caused error
}

interface ErrorDetail {
  field: string;                 // Field name that failed validation
  message: string;               // Specific error message for field
}
```

### Example Error Responses

**Validation Error (400)**:
```json
{
  "error": "Validation Error",
  "message": "Request validation failed",
  "details": [
    {
      "field": "title",
      "message": "Title is required and must be 1-200 characters"
    },
    {
      "field": "status",
      "message": "Status must be one of: pending, in_progress, completed"
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

**Authentication Error (401)**:
```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid authentication token",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

**Authorization Error (403)**:
```json
{
  "error": "Forbidden",
  "message": "You do not have permission to access this resource",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

**Not Found Error (404)**:
```json
{
  "error": "Not Found",
  "message": "Task not found",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

**Rate Limit Error (429)**:
```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Please try again later.",
  "details": [
    {
      "field": "rate_limit",
      "message": "Maximum 100 requests per minute exceeded"
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

**Server Error (500)**:
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/tasks"
}
```

### Error Response Headers

All error responses include:
```
Content-Type: application/json
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
```

---

## 5. HTTP Status Codes

### Success Codes

| Code | Status | Usage |
|------|--------|-------|
| 200 | OK | Successful GET, PUT, PATCH requests |
| 201 | Created | Successful POST request (task created) |
| 204 | No Content | Successful DELETE request |

### Client Error Codes

| Code | Status | Usage |
|------|--------|-------|
| 400 | Bad Request | Invalid request format, validation errors, malformed JSON |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | Valid JWT but insufficient permissions (wrong user) |
| 404 | Not Found | Resource not found or inaccessible |
| 422 | Unprocessable Entity | Valid JSON but semantic errors (schema mismatch) |
| 429 | Too Many Requests | Rate limit exceeded |

### Server Error Codes

| Code | Status | Usage |
|------|--------|-------|
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Temporary service outage (database down, maintenance) |

### Status Code Decision Tree

```
Request received
│
├─ Valid JWT token?
│  ├─ No → 401 Unauthorized
│  └─ Yes → Continue
│
├─ Resource exists?
│  ├─ No → 404 Not Found
│  └─ Yes → Continue
│
├─ User owns resource?
│  ├─ No → 403 Forbidden (or 404 for security)
│  └─ Yes → Continue
│
├─ Valid request format?
│  ├─ No → 400 Bad Request or 422 Unprocessable Entity
│  └─ Yes → Continue
│
├─ Rate limit OK?
│  ├─ No → 429 Too Many Requests
│  └─ Yes → Continue
│
├─ Operation successful?
│  ├─ No → 500 Internal Server Error
│  └─ Yes → 200/201/204 Success
```

---

## 6. Design Decisions

### 6.1 User ID in JWT vs URL Path

**Decision**: User ID is extracted from JWT token, NOT included in URL path.

#### Recommended Pattern (Implemented)

```http
GET /api/tasks
Authorization: Bearer {jwt_token containing user_id}
```

**Benefits**:
1. **Security**: No user ID in URL prevents enumeration attacks
2. **Simplicity**: Cleaner URLs, easier to use
3. **Consistency**: All endpoints follow same pattern
4. **Authorization**: User can only access their own tasks (automatic)
5. **URL Stability**: User ID change doesn't break URLs
6. **Logging**: Sensitive user IDs not in access logs

**Implementation**:
```python
# Backend extracts user_id from JWT
@router.get("/api/tasks")
async def get_tasks(current_user: User = Depends(get_current_user)):
    user_id = current_user.id  # From JWT
    tasks = await task_service.get_tasks_by_user(user_id)
    return tasks
```

#### Alternative Pattern (NOT Recommended)

```http
GET /api/{user_id}/tasks
Authorization: Bearer {jwt_token}
```

**Drawbacks**:
1. **Security Risk**: Exposes user IDs in URLs (enumeration attack surface)
2. **Complexity**: Must validate URL user_id matches JWT user_id
3. **Inconsistency**: Redundant information (in both URL and JWT)
4. **Audit Trail**: User IDs appear in logs, proxies, browser history
5. **Client Complexity**: Client must track and inject user_id

**When This Pattern Is Valid**:
- Admin endpoints accessing other users' data
- Multi-tenant systems with workspace/organization IDs
- Public APIs with user profiles (GET /users/{user_id}/profile)

**Example Admin Endpoint** (valid use case):
```http
GET /api/admin/users/{user_id}/tasks
Authorization: Bearer {admin_jwt_token}
```

### 6.2 REST API Design Principles

**Resource-Oriented URLs**:
- `/api/tasks` - Collection
- `/api/tasks/{id}` - Individual resource
- `/api/tasks/{id}/complete` - Action on resource

**HTTP Methods Map to CRUD**:
- POST → Create
- GET → Read
- PUT → Update (full replacement)
- PATCH → Update (partial)
- DELETE → Delete

**Stateless Authentication**:
- JWT in Authorization header
- No server-side session storage
- Each request self-contained

**Consistent Response Structure**:
- Success: Resource representation
- Error: Standard error object
- Pagination: Metadata included

### 6.3 API Versioning Strategy

**URL Path Versioning**: `/api/v1/tasks`

**Rationale**:
- Clear, explicit versioning
- Easy to route different versions
- Browser-friendly (no headers needed)
- Standard industry practice

**Alternatives Considered**:
- Header versioning: `Accept: application/vnd.evolution-todo.v1+json`
  - Rejected: Less visible, harder to debug
- Query parameter: `/api/tasks?version=1`
  - Rejected: Pollutes query string, easy to omit

### 6.4 Pagination Strategy

**Offset-based Pagination**: `?page=1&limit=20`

**Rationale**:
- Simple to implement and understand
- Works well for small-medium datasets
- Supports random page access

**Limitations**:
- Performance degrades with large offsets
- Inconsistent results if data changes during pagination

**Future Enhancement**: Consider cursor-based pagination for scale:
```
GET /api/tasks?cursor=eyJpZCI6IjEyMyJ9&limit=20
```

### 6.5 Error Handling Philosophy

**Consistent Error Format**: All errors follow same schema

**Helpful Error Messages**:
- Clear, actionable messages
- Field-level validation details
- No sensitive information leakage

**Security Considerations**:
- 404 for unauthorized access (not 403) to prevent enumeration
- Generic 500 messages (detailed logs server-side only)
- No stack traces in production

---

## 7. Cross-References

### Related Specifications

**Features**:
- **specs/phase-2-todo-web/features/authentication.md** - JWT authentication flow
- **specs/phase-2-todo-web/features/task-crud.md** - Task CRUD business logic
- **specs/phase-2-todo-web/features/task-filtering.md** - Search and filter requirements

**API**:
- **specs/phase-2-todo-web/api/auth-endpoints.md** - Login, signup, token refresh endpoints
- **specs/phase-2-todo-web/api/health-endpoints.md** - Health check and status endpoints

**Database**:
- **specs/phase-2-todo-web/database/tasks-schema.md** - Task table schema and indexes
- **specs/phase-2-todo-web/database/users-schema.md** - User table schema

**UI**:
- **specs/phase-2-todo-web/ui/task-list-page.md** - Frontend task list component
- **specs/phase-2-todo-web/ui/task-form.md** - Create/edit task form

### Architecture Decision Records

- **history/adr/001-jwt-authentication.md** - JWT token strategy
- **history/adr/002-rest-api-design.md** - RESTful API patterns
- **history/adr/003-user-isolation.md** - User data isolation approach

### Implementation Guides

- **apps/backend/CLAUDE.md** - FastAPI backend implementation guide
- **apps/frontend/CLAUDE.md** - Next.js frontend API integration guide
- **.claude/skills/skills.md** - API implementation skills

---

## 8. OpenAPI Documentation

### Auto-Generated Documentation

FastAPI automatically generates OpenAPI 3.0 specification and interactive documentation.

**Swagger UI**: `http://localhost:8000/docs`
- Interactive API explorer
- Try endpoints directly in browser
- View request/response schemas

**ReDoc**: `http://localhost:8000/redoc`
- Clean, readable documentation
- Better for reading than testing
- Organized by tags

### OpenAPI Schema Export

Download OpenAPI JSON schema:
```http
GET /openapi.json
```

Use for:
- Frontend type generation (openapi-typescript)
- API client generation (openapi-generator)
- Contract testing
- Documentation publishing

### Example OpenAPI Schema

```yaml
openapi: 3.0.0
info:
  title: Evolution Todo API
  version: 1.0.0
  description: RESTful API for Evolution Todo application

servers:
  - url: http://localhost:8000
    description: Development server
  - url: https://api.evolution-todo.railway.app
    description: Production server

paths:
  /api/tasks:
    get:
      summary: Get all tasks
      operationId: getTasks
      tags:
        - Tasks
      security:
        - BearerAuth: []
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, in_progress, completed, all]
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetTasksResponse'
        '401':
          $ref: '#/components/responses/UnauthorizedError'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    Task:
      type: object
      properties:
        id:
          type: string
          format: uuid
        user_id:
          type: string
          format: uuid
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 2000
          nullable: true
        status:
          type: string
          enum: [pending, in_progress, completed]
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
```

### Type Generation for Frontend

Generate TypeScript types from OpenAPI schema:

```bash
# Install openapi-typescript
npm install --save-dev openapi-typescript

# Generate types
npx openapi-typescript http://localhost:8000/openapi.json -o src/types/api.ts
```

Use generated types:
```typescript
import type { paths } from '@/types/api';

type GetTasksResponse = paths['/api/tasks']['get']['responses']['200']['content']['application/json'];
type CreateTaskRequest = paths['/api/tasks']['post']['requestBody']['content']['application/json'];
```

---

## 9. Testing & Validation

### Test Coverage Requirements

All endpoints must have:
1. **Unit Tests**: Service layer validation
2. **Integration Tests**: Full request/response cycle
3. **E2E Tests**: Frontend-backend integration

### Example Test Cases

**GET /api/tasks**:
- ✅ Returns empty array for new user
- ✅ Returns all tasks for authenticated user
- ✅ Filters by status correctly
- ✅ Paginates results correctly
- ✅ Searches title and description
- ✅ Returns 401 without JWT
- ✅ Does not return other users' tasks

**POST /api/tasks**:
- ✅ Creates task with valid data
- ✅ Returns 201 with created task
- ✅ Auto-generates UUID
- ✅ Sets created_at and updated_at
- ✅ Extracts user_id from JWT
- ✅ Returns 400 for missing title
- ✅ Returns 400 for title > 200 chars
- ✅ Returns 400 for invalid status
- ✅ Trims whitespace from title

**DELETE /api/tasks/{id}**:
- ✅ Deletes task successfully
- ✅ Returns 204 No Content
- ✅ Returns 404 for non-existent task
- ✅ Returns 403 for other user's task
- ✅ Returns 400 for invalid UUID

### API Testing Tools

**Development**:
- Swagger UI (`/docs`) - Interactive testing
- cURL - Command-line testing
- Postman - API client
- HTTPie - User-friendly HTTP client

**Automated Testing**:
- Pytest + httpx (backend integration tests)
- Playwright (E2E tests)
- Jest + MSW (frontend API mocking)

### Example Integration Test

```python
# tests/integration/test_tasks_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_and_get_task(client: AsyncClient, auth_token: str):
    # Create task
    response = await client.post(
        "/api/tasks",
        json={
            "title": "Test task",
            "description": "Test description",
            "status": "pending"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    task = response.json()
    assert task["title"] == "Test task"

    # Get task
    response = await client.get(
        f"/api/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    retrieved = response.json()
    assert retrieved["id"] == task["id"]
```

---

## 10. Performance Considerations

### Database Indexes

```sql
-- Primary key
CREATE INDEX idx_tasks_id ON tasks(id);

-- User isolation queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Filtering and sorting
CREATE INDEX idx_tasks_user_status_created ON tasks(user_id, status, created_at DESC);

-- Search (PostgreSQL full-text search)
CREATE INDEX idx_tasks_search ON tasks USING gin(to_tsvector('english', title || ' ' || description));
```

### Caching Strategy

**Client-Side** (Frontend):
- SWR/React Query with stale-while-revalidate
- Cache duration: 5 minutes
- Revalidate on focus/reconnect

**Server-Side** (Backend):
- Redis cache for frequently accessed tasks
- Cache invalidation on updates
- TTL: 1 minute

### Response Time Targets

| Endpoint | Target | Max |
|----------|--------|-----|
| GET /api/tasks | < 100ms | 500ms |
| POST /api/tasks | < 200ms | 1s |
| GET /api/tasks/{id} | < 50ms | 200ms |
| PUT/PATCH /api/tasks/{id} | < 150ms | 500ms |
| DELETE /api/tasks/{id} | < 100ms | 500ms |

### Pagination Limits

- **Default**: 20 items per page
- **Maximum**: 100 items per page
- **Rationale**: Balance between payload size and number of requests

---

## Changelog

### Version 1.0 (2026-01-08)
- Initial specification
- Defined all task CRUD endpoints
- Established authentication pattern (JWT, no user_id in URL)
- Documented error handling standards
- Added design decision rationale

---

**Specification Status**: Draft
**Next Steps**:
1. Review and approve API design
2. Generate OpenAPI schema
3. Implement backend endpoints (see `/sp.tasks`)
4. Create integration tests
5. Document in Swagger/ReDoc

**Related Commands**:
- `/sp.plan` - Generate architecture plan from this spec
- `/sp.tasks` - Break down into implementation tasks
- `/sp.adr` - Document architectural decisions
