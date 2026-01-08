# Feature Specification: User Authentication & Authorization

**Feature Branch**: `002-authentication-jwt`
**Created**: 2026-01-08
**Status**: Draft
**Technology**: Better Auth + JWT (JSON Web Tokens)

## Overview

This specification defines the authentication and authorization system for the Evolution of Todo Phase II application. It implements user registration, login, session management, and user-specific data isolation using Better Auth library with JWT tokens. The system ensures that each user can only access and manage their own todo items through secure, token-based authentication.

**Business Value**: Enables multi-user support with secure access control, allowing the application to scale from single-user to multi-tenant SaaS deployment while maintaining data privacy and security.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration (Priority: P1)

A new user visits the application and creates an account to start managing their personal todo list securely.

**Why this priority**: Registration is the entry point for all user interactions. Without user accounts, we cannot implement user-specific data isolation or any authenticated features.

**Independent Test**: Can be fully tested by submitting a registration form with valid credentials and verifying that a new user record is created in the database with hashed password. Delivers immediate value by allowing users to create accounts.

**Acceptance Scenarios**:

1. **Given** I am on the registration page, **When** I submit valid email and password (meeting all requirements), **Then** my account is created, I receive a JWT token in an httpOnly cookie, and I am redirected to the todo list page
2. **Given** I am on the registration page, **When** I submit an email that already exists, **Then** I see an error message "Email already registered" and registration fails
3. **Given** I am on the registration page, **When** I submit a password that doesn't meet strength requirements, **Then** I see specific validation errors (e.g., "Password must be at least 8 characters") and registration fails
4. **Given** I am on the registration page, **When** I submit an invalid email format, **Then** I see error message "Invalid email format" and registration fails
5. **Given** I successfully register, **When** I check the database, **Then** my password is stored as a bcrypt hash (not plaintext)

---

### User Story 2 - User Login (Priority: P1)

A returning user accesses the application and logs in with their credentials to access their personal todo list.

**Why this priority**: Login is equally critical as registration - existing users must be able to authenticate to access their data. Without login, user accounts are useless.

**Independent Test**: Can be fully tested by submitting login credentials for an existing user and verifying JWT token issuance and redirection to protected routes. Delivers immediate value by granting access to existing users.

**Acceptance Scenarios**:

1. **Given** I have a registered account, **When** I submit correct email and password, **Then** I receive a JWT token, my session is established, and I am redirected to my todo list
2. **Given** I have a registered account, **When** I submit incorrect password, **Then** I see error message "Invalid credentials" and login fails
3. **Given** I submit credentials for a non-existent email, **When** I attempt to login, **Then** I see error message "Invalid credentials" (same as wrong password for security)
4. **Given** I successfully login, **When** I examine the response, **Then** I have an httpOnly cookie containing my JWT token with expiration set to 7 days
5. **Given** I am already logged in, **When** I navigate to the login page, **Then** I am automatically redirected to the todo list page

---

### User Story 3 - Protected Route Access with JWT Validation (Priority: P1)

A logged-in user accesses protected pages (todo list, profile) and the system validates their JWT token on every request to ensure continuous authentication.

**Why this priority**: Core security requirement - all authenticated features depend on proper token validation. Without this, user isolation and authorization cannot work.

**Independent Test**: Can be fully tested by attempting to access protected routes with valid/invalid/expired tokens and verifying proper access control. Delivers immediate security value by enforcing authentication.

**Acceptance Scenarios**:

1. **Given** I am logged in with a valid JWT token, **When** I access the todo list page, **Then** the system validates my token, extracts my user ID, and displays only my todos
2. **Given** I have no JWT token (not logged in), **When** I try to access a protected route (e.g., /todos), **Then** I am redirected to the login page
3. **Given** I have an expired JWT token, **When** I make an API request, **Then** I receive a 401 Unauthorized response and am redirected to login
4. **Given** I have a malformed or tampered JWT token, **When** I make an API request, **Then** I receive a 401 Unauthorized response and my session is terminated
5. **Given** I am logged in, **When** my JWT token expires (after 7 days), **Then** I am automatically logged out and redirected to login on the next request

---

### User Story 4 - User-Specific Data Isolation (Priority: P1)

Each user can only view, create, update, and delete their own todo items, ensuring complete data privacy between users.

**Why this priority**: Critical security requirement that ensures data privacy. Without this, the multi-user system would leak data between users, making it unusable and insecure.

**Independent Test**: Can be fully tested by creating todos as User A, logging in as User B, and verifying User B cannot access User A's todos via UI or API. Delivers immediate security value.

**Acceptance Scenarios**:

1. **Given** I am logged in as User A, **When** I create a todo, **Then** it is associated with my user ID in the database
2. **Given** I am logged in as User A, **When** I fetch my todo list, **Then** I only see todos where user_id matches my ID
3. **Given** I am logged in as User B, **When** I try to access User A's todo via API (e.g., GET /api/tasks/{user_a_task_id}), **Then** I receive a 403 Forbidden response
4. **Given** I am logged in as User B, **When** I try to modify User A's todo via API (e.g., PUT /api/tasks/{user_a_task_id}), **Then** I receive a 403 Forbidden response
5. **Given** I am logged in, **When** I make any database query for todos, **Then** the query automatically filters by my user_id (database-level isolation)

---

### User Story 5 - User Logout (Priority: P2)

A logged-in user can securely log out, invalidating their session and clearing authentication state.

**Why this priority**: Important for security (especially on shared devices) but not critical for MVP functionality. Users can still use the app without logout if needed.

**Independent Test**: Can be fully tested by logging out and verifying that the JWT token is cleared and subsequent requests to protected routes are denied. Delivers security value for shared/public devices.

**Acceptance Scenarios**:

1. **Given** I am logged in, **When** I click the logout button, **Then** my JWT cookie is cleared, my client-side auth state is reset, and I am redirected to the login page
2. **Given** I just logged out, **When** I try to access a protected route, **Then** I am redirected to the login page (token is no longer valid)
3. **Given** I just logged out, **When** I click the browser back button, **Then** I cannot access previously viewed protected pages (proper cache control)
4. **Given** I am logged in on multiple devices, **When** I logout on one device, **Then** only that device's session is terminated (other devices remain logged in)

---

### User Story 6 - JWT Token Refresh (Priority: P2)

Users with expiring JWT tokens can automatically refresh them to maintain continuous access without re-authentication.

**Why this priority**: Improves user experience by preventing unexpected logouts, but not critical for MVP. Initial implementation can use longer-lived tokens without refresh.

**Independent Test**: Can be fully tested by simulating a token near expiration and verifying automatic refresh occurs before expiration. Delivers UX value by preventing interruptions.

**Acceptance Scenarios**:

1. **Given** my JWT token will expire in 1 hour, **When** I make an API request, **Then** the system issues a new token with extended expiration and updates my cookie
2. **Given** my JWT token has expired, **When** I try to refresh it, **Then** I must re-authenticate (refresh only works for non-expired tokens within refresh window)
3. **Given** I have a valid refresh token, **When** I request a new access token, **Then** I receive a fresh JWT without re-entering credentials
4. **Given** I logout, **When** my refresh token is checked, **Then** it is invalidated and cannot be used to obtain new access tokens

---

### User Story 7 - Password Change (Priority: P3)

A logged-in user can change their password for account security.

**Why this priority**: Important for long-term security but not required for initial MVP. Can be added after core authentication is stable.

**Independent Test**: Can be fully tested by submitting a password change request with old and new passwords, then verifying the new password works for login. Delivers account management value.

**Acceptance Scenarios**:

1. **Given** I am logged in, **When** I submit my current password and a new password (meeting requirements), **Then** my password is updated and I can login with the new password
2. **Given** I am on the password change page, **When** I submit an incorrect current password, **Then** I see error message "Current password is incorrect"
3. **Given** I successfully change my password, **When** I check the database, **Then** the new password hash is different from the old hash
4. **Given** I change my password, **When** the change is successful, **Then** I receive a confirmation email notification (optional security feature)

---

### Edge Cases

**Authentication Edge Cases**:
- What happens when a user tries to register with an email that was previously registered but deleted?
  - **Expected**: System treats deleted accounts as available and allows re-registration with same email
- What happens when JWT secret key is rotated (changed)?
  - **Expected**: All existing tokens become invalid, users must re-login
- What happens when a user's token is valid but their account has been deleted/disabled?
  - **Expected**: Token validation checks user status in DB; returns 401 if account is inactive
- What happens when a user submits 100 failed login attempts in 1 minute?
  - **Expected**: Rate limiting blocks IP address after 5 failed attempts for 15 minutes
- What happens when multiple users register with the same email simultaneously (race condition)?
  - **Expected**: Database unique constraint ensures only one succeeds, others receive "Email already registered" error

**Token Security Edge Cases**:
- What happens when someone tries to use a JWT token from a different user?
  - **Expected**: Token is valid cryptographically but user_id won't match, leading to 403 errors when accessing resources
- What happens when someone modifies the payload of a JWT token?
  - **Expected**: Signature verification fails, token is rejected as invalid
- What happens when the client's system clock is wrong (causing token expiration issues)?
  - **Expected**: Server time is source of truth; tokens validated against server time only
- What happens when a user's browser doesn't support cookies?
  - **Expected**: Application displays error message requiring cookie support for authentication

**Data Isolation Edge Cases**:
- What happens when a user manually crafts an API request with another user's task ID?
  - **Expected**: Backend validates user_id from JWT matches task.user_id; returns 403 Forbidden if mismatch
- What happens when database query accidentally omits user_id filter?
  - **Expected**: Middleware/decorator enforces user_id filtering at framework level as safety net
- What happens when an admin role is introduced and needs to see all users' tasks?
  - **Expected**: Authorization layer checks role permissions; admin role bypasses user_id filtering

**Session Management Edge Cases**:
- What happens when a user leaves a tab open for 8 days (beyond token expiration)?
  - **Expected**: Next API request returns 401; frontend detects and redirects to login page
- What happens when a user clears their cookies mid-session?
  - **Expected**: User immediately appears logged out; next navigation to protected route redirects to login
- What happens when httpOnly cookies are blocked by browser security settings?
  - **Expected**: Fallback to localStorage for token storage (less secure but functional)

## Requirements *(mandatory)*

### Functional Requirements

**User Registration**:
- **FR-001**: System MUST allow users to register with email and password
- **FR-002**: System MUST validate email format using regex pattern: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- **FR-003**: System MUST enforce password requirements: minimum 8 characters, at least 1 uppercase, 1 lowercase, 1 number, 1 special character
- **FR-004**: System MUST check for email uniqueness before creating account (case-insensitive)
- **FR-005**: System MUST hash passwords using bcrypt with salt rounds = 10 before storage
- **FR-006**: System MUST NOT store plaintext passwords in database or logs

**User Login**:
- **FR-007**: System MUST authenticate users via email and password credentials
- **FR-008**: System MUST generate JWT token containing user_id, email, and issued_at timestamp upon successful login
- **FR-009**: System MUST sign JWT tokens with HS256 algorithm using secure secret key (minimum 32 characters)
- **FR-010**: System MUST set JWT token expiration to 7 days (604800 seconds)
- **FR-011**: System MUST store JWT token in httpOnly cookie with Secure and SameSite=Strict flags
- **FR-012**: System MUST return generic "Invalid credentials" error for both wrong email and wrong password (security by obscurity)

**Session Management**:
- **FR-013**: System MUST validate JWT token on every request to protected routes
- **FR-014**: System MUST extract user_id from validated JWT token for all authenticated operations
- **FR-015**: System MUST return 401 Unauthorized for expired, malformed, or missing JWT tokens
- **FR-016**: System MUST check token expiration using current server time (UTC)
- **FR-017**: System MUST verify JWT signature matches expected secret key

**User Logout**:
- **FR-018**: System MUST provide logout endpoint that clears JWT cookie
- **FR-019**: System MUST set cookie expiration to past date on logout (effectively deleting it)
- **FR-020**: System MUST clear client-side authentication state on logout

**User-Specific Data Isolation**:
- **FR-021**: System MUST associate every todo item with the user_id of its creator
- **FR-022**: System MUST filter all todo queries by authenticated user's user_id
- **FR-023**: System MUST validate user_id matches resource owner before allowing update/delete operations
- **FR-024**: System MUST return 403 Forbidden when user attempts to access another user's resources
- **FR-025**: System MUST enforce user isolation at API middleware level (not just UI)

**Security**:
- **FR-026**: System MUST implement rate limiting on auth endpoints: max 5 login attempts per IP per 15 minutes
- **FR-027**: System MUST use HTTPS-only cookies in production environment
- **FR-028**: System MUST sanitize all user inputs to prevent XSS attacks
- **FR-029**: System MUST implement CORS policy allowing only configured frontend origins
- **FR-030**: System MUST set security headers: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection
- **FR-031**: System MUST log authentication events (login, logout, failed attempts) for security audit

**Frontend Integration**:
- **FR-032**: Frontend MUST use Better Auth client library for authentication state management
- **FR-033**: Frontend MUST redirect unauthenticated users to /login when accessing protected routes
- **FR-034**: Frontend MUST display loading state while verifying authentication status
- **FR-035**: Frontend MUST persist authentication state across page refreshes
- **FR-036**: Frontend MUST provide clear visual indication of logged-in status (e.g., user menu)

### Key Entities

- **User**: Represents an authenticated user account
  - Attributes: id (UUID), email (unique, indexed), password_hash (bcrypt), created_at, updated_at
  - Relationships: One-to-many with Task (a user has many tasks)

- **Task/Todo**: Represents a todo item (existing entity from Phase I, now user-scoped)
  - Attributes: id, user_id (foreign key to User), title, description, status, created_at, updated_at
  - Relationships: Many-to-one with User (a task belongs to one user)

- **JWT Token**: Represents an authentication token (not stored in DB, exists as signed string)
  - Payload: user_id, email, issued_at (iat), expiration (exp)
  - Security: Signed with HS256, validated on every request

## Validation Rules

### Email Validation
- **Type**: String
- **Required**: True
- **Constraints**:
  - Min length: 5 characters (e.g., "a@b.c")
  - Max length: 254 characters (RFC 5321)
  - Pattern: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
  - Case handling: Convert to lowercase before storage/lookup
- **Transforms**: Trim whitespace, convert to lowercase
- **Error Messages**:
  - Required: "Email is required"
  - Invalid format: "Invalid email format. Please enter a valid email address (e.g., user@example.com)"
  - Already exists: "An account with this email already exists. Please login or use a different email."
  - Too long: "Email must be less than 254 characters"

### Password Validation (Registration/Change)
- **Type**: String
- **Required**: True
- **Constraints**:
  - Min length: 8 characters
  - Max length: 128 characters
  - Must contain: At least 1 uppercase letter (A-Z)
  - Must contain: At least 1 lowercase letter (a-z)
  - Must contain: At least 1 number (0-9)
  - Must contain: At least 1 special character (!@#$%^&*()_+-=[]{}|;:,.<>?)
  - Pattern: `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:,.<>?])[A-Za-z\d!@#$%^&*()_+\-=\[\]{}|;:,.<>?]{8,128}$`
- **Transforms**: No transforms (preserve exact password)
- **Error Messages**:
  - Required: "Password is required"
  - Too short: "Password must be at least 8 characters long"
  - Too long: "Password must be less than 128 characters"
  - Missing uppercase: "Password must contain at least one uppercase letter"
  - Missing lowercase: "Password must contain at least one lowercase letter"
  - Missing number: "Password must contain at least one number"
  - Missing special char: "Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)"
  - Invalid format: "Password does not meet security requirements. Please ensure it contains uppercase, lowercase, number, and special character."

### Current Password Validation (Password Change)
- **Type**: String
- **Required**: True (for password change operation)
- **Constraints**: Must match user's stored password hash
- **Error Messages**:
  - Required: "Current password is required"
  - Incorrect: "Current password is incorrect"

### Login Credentials Validation
- **Email**: Same as registration email validation
- **Password**:
  - Type: String
  - Required: True
  - Min length: 1 (no validation rules on login, only hash comparison)
  - Error Messages:
    - Required: "Password is required"
    - Invalid credentials: "Invalid email or password" (generic error for security)

### JWT Token Validation
- **Type**: String (JWT format)
- **Required**: True (for protected routes)
- **Constraints**:
  - Must be valid JWT format (header.payload.signature)
  - Signature must verify with server secret key
  - Must not be expired (exp claim < current time)
  - Must contain required claims: user_id, email, iat, exp
- **Error Messages**:
  - Missing: "Authentication required. Please login to continue."
  - Invalid/Malformed: "Invalid authentication token. Please login again."
  - Expired: "Your session has expired. Please login again."
  - Invalid signature: "Invalid authentication token. Please login again."

## Business Rules

1. **Email Uniqueness**: No two active users can have the same email address (case-insensitive)
2. **Password Security**: Passwords must never be stored in plaintext; only bcrypt hashes are persisted
3. **Token Expiration**: JWT tokens expire after 7 days; users must re-authenticate after expiration
4. **User Isolation**: Users can ONLY access resources (todos) where user_id matches their authenticated user_id
5. **Rate Limiting**: Maximum 5 failed login attempts per IP address within 15-minute window
6. **Generic Error Messages**: Login errors must not reveal whether email exists (use "Invalid credentials" for both cases)
7. **HTTPS Enforcement**: httpOnly cookies must have Secure flag set to true in production (HTTPS only)
8. **Cookie Security**: JWT cookies must use SameSite=Strict to prevent CSRF attacks
9. **Session Validation**: Every request to protected routes must validate JWT token freshness and signature
10. **Account Deletion**: If user account is deleted, all associated todos must be cascade deleted or reassigned
11. **Token Storage**: Frontend must NEVER access JWT token directly (httpOnly prevents JavaScript access)
12. **CORS Policy**: Backend must only accept requests from configured frontend origins
13. **Audit Logging**: All authentication events (login, logout, failed attempts) must be logged with timestamp and IP
14. **Password Reset**: Password change requires current password verification (prevents session hijacking password changes)
15. **Token Refresh Window**: Token refresh is only allowed within 1 hour before expiration (not after expiration)

## Examples

### Valid Registration Request

**Frontend Form Submission**:
```typescript
// POST /api/auth/register
{
  "email": "john.doe@example.com",
  "password": "SecureP@ss123"
}
```

**Backend Response (Success)**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@example.com",
    "created_at": "2026-01-08T14:30:00Z"
  },
  "message": "Registration successful"
}
```

**Set-Cookie Header**:
```
Set-Cookie: auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=604800
```

---

### Invalid Registration Examples

**Example 1: Weak Password**
```typescript
// Request
{
  "email": "user@example.com",
  "password": "weak"
}

// Response (400 Bad Request)
{
  "error": "Validation failed",
  "details": {
    "password": [
      "Password must be at least 8 characters long",
      "Password must contain at least one uppercase letter",
      "Password must contain at least one number",
      "Password must contain at least one special character"
    ]
  }
}
```

**Example 2: Invalid Email**
```typescript
// Request
{
  "email": "invalid-email",
  "password": "SecureP@ss123"
}

// Response (400 Bad Request)
{
  "error": "Validation failed",
  "details": {
    "email": ["Invalid email format. Please enter a valid email address (e.g., user@example.com)"]
  }
}
```

**Example 3: Duplicate Email**
```typescript
// Request
{
  "email": "existing@example.com",
  "password": "SecureP@ss123"
}

// Response (409 Conflict)
{
  "error": "An account with this email already exists. Please login or use a different email."
}
```

---

### Valid Login Request

**Frontend Form Submission**:
```typescript
// POST /api/auth/login
{
  "email": "john.doe@example.com",
  "password": "SecureP@ss123"
}
```

**Backend Response (Success)**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@example.com"
  },
  "message": "Login successful"
}
```

**Set-Cookie Header** (same as registration)

---

### Invalid Login Examples

**Example 1: Wrong Password**
```typescript
// Request
{
  "email": "john.doe@example.com",
  "password": "WrongPassword123"
}

// Response (401 Unauthorized)
{
  "error": "Invalid email or password"
}
```

**Example 2: Non-existent Email**
```typescript
// Request
{
  "email": "nonexistent@example.com",
  "password": "SecureP@ss123"
}

// Response (401 Unauthorized) - Same error for security
{
  "error": "Invalid email or password"
}
```

**Example 3: Rate Limit Exceeded**
```typescript
// Request (after 5 failed attempts)
{
  "email": "john.doe@example.com",
  "password": "WrongPassword123"
}

// Response (429 Too Many Requests)
{
  "error": "Too many login attempts. Please try again in 15 minutes.",
  "retry_after": 900
}
```

---

### Protected Route Access

**Valid Request with JWT**:
```typescript
// GET /api/tasks
// Cookie: auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

// Response (200 OK)
{
  "tasks": [
    {
      "id": 1,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "status": "pending"
    }
  ]
}
```

**Invalid Request (No Token)**:
```typescript
// GET /api/tasks
// (No auth_token cookie)

// Response (401 Unauthorized)
{
  "error": "Authentication required. Please login to continue.",
  "redirect": "/login"
}
```

**Invalid Request (Expired Token)**:
```typescript
// GET /api/tasks
// Cookie: auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (expired)

// Response (401 Unauthorized)
{
  "error": "Your session has expired. Please login again.",
  "redirect": "/login"
}
```

---

### User Isolation Example

**Scenario**: User A (id=user-a-id) tries to access User B's task (id=task-123, user_id=user-b-id)

```typescript
// GET /api/tasks/task-123
// Cookie: auth_token=<User A's valid token>

// Response (403 Forbidden)
{
  "error": "Access denied. You do not have permission to access this resource."
}
```

---

### Logout Request

```typescript
// POST /api/auth/logout
// Cookie: auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

// Response (200 OK)
{
  "message": "Logout successful"
}

// Set-Cookie Header (clears cookie)
Set-Cookie: auth_token=; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=0; Expires=Thu, 01 Jan 1970 00:00:00 GMT
```

## Non-Functional Requirements

### Performance
- **NFR-001**: Authentication endpoint response time MUST be < 200ms at 95th percentile
- **NFR-002**: JWT token validation MUST complete in < 10ms per request
- **NFR-003**: Password hashing MUST use bcrypt with exactly 10 salt rounds (balance security and performance)
- **NFR-004**: System MUST handle 100 concurrent login requests without degradation

### Security
- **NFR-005**: All passwords MUST be hashed using bcrypt with minimum cost factor 10
- **NFR-006**: JWT secret key MUST be minimum 32 characters, randomly generated
- **NFR-007**: HTTPS MUST be enforced in production (no HTTP allowed)
- **NFR-008**: Cookies MUST use httpOnly, Secure, and SameSite=Strict flags in production
- **NFR-009**: Rate limiting MUST block excessive login attempts (max 5 per 15 min per IP)
- **NFR-010**: Authentication logs MUST include timestamp, IP address, user agent, and outcome

### Accessibility
- **NFR-011**: Login and registration forms MUST be keyboard navigable (TAB order logical)
- **NFR-012**: Error messages MUST be announced by screen readers (ARIA live regions)
- **NFR-013**: Password visibility toggle MUST have clear ARIA labels
- **NFR-014**: Forms MUST have clear focus indicators (visible focus ring)
- **NFR-015**: Color MUST NOT be the only indicator of error states (use icons + text)

### Usability
- **NFR-016**: Password validation errors MUST appear in real-time as user types
- **NFR-017**: Email validation MUST trigger on blur (not on every keystroke)
- **NFR-018**: Loading states MUST appear for operations taking > 200ms
- **NFR-019**: Success messages MUST auto-dismiss after 3 seconds
- **NFR-020**: Error messages MUST persist until user takes action

### Browser Compatibility
- **NFR-021**: Authentication MUST work in Chrome, Firefox, Safari, Edge (latest 2 versions)
- **NFR-022**: httpOnly cookies MUST be supported (fallback to localStorage if not)
- **NFR-023**: JavaScript MUST be enabled (no graceful degradation for auth)

### Monitoring & Observability
- **NFR-024**: Failed login attempts MUST be logged with IP address for security monitoring
- **NFR-025**: Authentication success rate MUST be tracked (target: > 95% for valid credentials)
- **NFR-026**: Token expiration events MUST be logged for analytics
- **NFR-027**: Rate limit violations MUST trigger security alerts

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete registration in under 60 seconds with valid credentials
- **SC-002**: Login success rate for valid credentials MUST be > 99% (excluding user errors)
- **SC-003**: 95% of users successfully authenticate on first attempt with correct credentials
- **SC-004**: Zero instances of users accessing other users' todo items (100% isolation)
- **SC-005**: Password validation provides clear, actionable feedback within 100ms
- **SC-006**: JWT token validation adds < 20ms latency to API requests
- **SC-007**: Zero plaintext passwords in database, logs, or error messages (100% compliance)
- **SC-008**: Rate limiting blocks 100% of brute force attempts (> 5 failures in 15 min)
- **SC-009**: Session persistence works across browser refresh for 7 days (token lifetime)
- **SC-010**: Logout successfully clears authentication state in < 100ms

### User Acceptance Criteria

- **UAC-001**: New users can create account and immediately access their empty todo list
- **UAC-002**: Returning users can login and see only their previously created todos
- **UAC-003**: Users attempting to access protected routes without login are redirected to login page
- **UAC-004**: Users receive clear, helpful error messages for all validation failures
- **UAC-005**: Users feel confident their data is private and secure (security indicators visible)

## Technical Architecture Notes

### Better Auth Integration

Better Auth is a modern authentication library that simplifies JWT implementation. Integration points:

**Frontend (Next.js)**:
- Install: `npm install better-auth`
- Create auth client in `/app/lib/auth-client.ts`
- Wrap app with `AuthProvider` in `/app/layout.tsx`
- Use `useAuth()` hook for authentication state
- Use `<ProtectedRoute>` component for route guards

**Backend (FastAPI)**:
- Install: `pip install better-auth-python` (or use custom JWT implementation)
- Create JWT utilities in `/app/core/security.py`
- Implement middleware in `/app/core/middleware/auth.py`
- Use `@requires_auth` decorator for protected endpoints
- Use `get_current_user()` dependency injection for user context

**Configuration**:
```typescript
// Frontend: apps/frontend/.env.local
NEXT_PUBLIC_AUTH_URL=http://localhost:8000/api/auth
NEXT_PUBLIC_API_URL=http://localhost:8000

// Backend: apps/backend/.env
JWT_SECRET_KEY=<32-char-random-secret>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=["http://localhost:3000"]
```

### Database Schema

**users table** (new):
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(254) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_email ON users(email);
```

**tasks table** (modified - add user_id foreign key):
```sql
ALTER TABLE tasks ADD COLUMN user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE;
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@example.com",
    "iat": 1704723000,
    "exp": 1705327800
  },
  "signature": "<HMAC-SHA256-signature>"
}
```

## Out of Scope

**Explicitly Excluded**:
- Social authentication (Google, GitHub, etc.) - Phase III feature
- Two-factor authentication (2FA/MFA) - Phase III security enhancement
- Password reset via email - Phase III feature (requires email service)
- Email verification on registration - Phase III feature
- Remember me / persistent sessions beyond 7 days - Not required for MVP
- User profile management (name, avatar, bio) - Phase III feature
- Account deletion by user - Phase III feature
- OAuth 2.0 / OpenID Connect - Phase III feature
- Role-based access control (RBAC) beyond user isolation - Phase III feature
- Session management across multiple devices with device list - Phase III feature
- WebAuthn / Passkeys - Future consideration
- Biometric authentication - Future consideration

**Deferred to Phase III**:
- Admin panel for user management
- User activity tracking and analytics
- Suspicious login detection (new device, location)
- Account lockout after repeated failed attempts (currently rate limiting only)
- Password strength meter UI (currently validation only)

## Dependencies

**External Libraries**:
- **Frontend**: better-auth, @better-auth/react, js-cookie (optional)
- **Backend**: PyJWT, bcrypt (or passlib with bcrypt), python-jose (alternative)
- **Database**: PostgreSQL with UUID extension

**Required Features/Services**:
- PostgreSQL database (Neon) must be provisioned before auth implementation
- HTTPS/SSL certificates for production (Vercel and Railway provide these)
- Environment variable management for JWT secrets

**Phase I Components**:
- None (authentication is new for Phase II)

**Phase II Components**:
- User database schema must exist
- API routing infrastructure must be in place
- Frontend routing system must support protected routes

## Constitution Alignment

This specification aligns with the project constitution:

**Spec-Driven Development (Principle I)**:
- Complete specification created before implementation
- All requirements traceable to user stories
- Implementation will strictly follow this spec

**Clean Code (Principle II)**:
- Type hints required for all Python authentication functions
- PEP 8 compliance for backend auth code
- TypeScript strict mode for frontend auth code

**Test-First Development (Principle III)**:
- TDD mandatory: Write failing tests for each acceptance scenario first
- Red-Green-Refactor for all authentication features
- 100% test coverage required for security-critical auth code

**Single Responsibility (Principle IV)**:
- Authentication logic separated from business logic
- User model separate from Task model
- JWT utilities isolated in security module
- Middleware handles auth concerns separately from routes

**Evolutionary Architecture (Principle V)**:
- Auth system designed to support future enhancements (OAuth, 2FA)
- User isolation enables future multi-tenancy
- JWT approach scales to microservices architecture

**User Experience First (Principle VI)**:
- Clear, actionable error messages for all validation failures
- Helpful feedback during registration (real-time validation)
- Intuitive login/logout flow with visual feedback
- Accessible forms with keyboard navigation and screen reader support

## References

- **Better Auth Documentation**: https://better-auth.com/docs
- **JWT Best Practices**: https://tools.ietf.org/html/rfc8725
- **OWASP Authentication Cheatsheet**: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- **bcrypt Specification**: https://en.wikipedia.org/wiki/Bcrypt
- **Next.js Authentication Patterns**: https://nextjs.org/docs/authentication
- **FastAPI Security**: https://fastapi.tiangolo.com/tutorial/security/

---

**Document Status**: Ready for Review
**Next Steps**:
1. Review and approve this specification
2. Run `/sp.plan` to generate architecture plan
3. Run `/sp.tasks` to break down into implementation tasks
4. Create ADR for authentication approach (Better Auth + JWT vs alternatives)
