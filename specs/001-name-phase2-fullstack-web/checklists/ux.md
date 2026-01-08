# UX & Accessibility Checklist

## User Experience

- [ ] Sign up flow is intuitive
- [ ] Sign in flow is straightforward
- [ ] Error messages are clear and actionable
- [ ] Success feedback provided (toasts/messages)
- [ ] Loading states shown during async operations
- [ ] Empty states have helpful messaging
- [ ] Forms have clear labels and placeholders
- [ ] Buttons have clear call-to-action text

## Task Management UX

- [ ] Creating task is quick (< 5 seconds)
- [ ] Toggling completion is instant (optimistic update)
- [ ] Editing task is intuitive
- [ ] Deleting task requires confirmation
- [ ] Filters are easy to understand
- [ ] Sort options are clear
- [ ] Task list is scannable

## Responsive Design

- [ ] Works on mobile (320px+)
- [ ] Works on tablet (768px+)
- [ ] Works on desktop (1024px+)
- [ ] Touch targets ≥44px on mobile
- [ ] Text readable on all screen sizes
- [ ] Forms usable on mobile
- [ ] Layouts adapt to screen size

## Accessibility (WCAG AA)

- [ ] Semantic HTML elements used
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible
- [ ] Color contrast ≥4.5:1 for text
- [ ] Images have alt text
- [ ] Forms have associated labels
- [ ] Error messages announced to screen readers
- [ ] ARIA labels on icon-only buttons

## Performance UX

- [ ] Initial page load < 2 seconds on 3G
- [ ] Task list renders quickly (< 500ms)
- [ ] Actions feel immediate (optimistic updates)
- [ ] No layout shift during loading
- [ ] Images optimized
- [ ] Fonts load without FOUT/FOIT

## Error Handling UX

- [ ] Network errors show retry option
- [ ] Validation errors show inline
- [ ] Server errors show friendly message
- [ ] 404 errors have helpful navigation
- [ ] Session expired redirects to login
