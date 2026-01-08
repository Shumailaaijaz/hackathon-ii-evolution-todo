# Performance Checklist

## API Performance

- [ ] GET /api/{user_id}/tasks responds in < 200ms (p95)
- [ ] POST /api/{user_id}/tasks responds in < 200ms (p95)
- [ ] PUT/PATCH endpoints respond in < 200ms (p95)
- [ ] DELETE endpoints respond in < 100ms (p95)
- [ ] Health check responds in < 50ms

## Database Performance

- [ ] Queries use indexes (user_id, completed, created_at)
- [ ] Query execution time < 50ms average
- [ ] Connection pooling configured (pool_size=5)
- [ ] No N+1 query problems
- [ ] Database connection reused

## Frontend Performance

- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 3s
- [ ] Largest Contentful Paint < 2.5s
- [ ] Cumulative Layout Shift < 0.1
- [ ] Initial bundle size < 200KB gzipped

## Caching & Optimization

- [ ] SWR caching configured
- [ ] Static assets cached (images, fonts)
- [ ] API responses cacheable where appropriate
- [ ] Optimistic updates for mutations
- [ ] Images optimized and lazy loaded

## Network Optimization

- [ ] API requests batched where possible
- [ ] Unnecessary re-fetches avoided
- [ ] Debouncing on search/filter inputs
- [ ] Pagination implemented for large lists
- [ ] Compression enabled (gzip/brotli)

## Monitoring

- [ ] Response time metrics tracked
- [ ] Error rates monitored
- [ ] Database query performance logged
- [ ] Frontend performance metrics collected
- [ ] Alerts configured for degradation
