# API Documentation

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

#### GET /health

Check API health and service status.

**Response:**
```json
{
  "status": "healthy",
  "workflow_initialized": true,
  "aws_credentials": {
    "ok": true,
    "message": "AWS credentials configured"
  },
  "bedrock_access": {
    "ok": true,
    "message": "Bedrock access available"
  },
  "cache_stats": {
    "total_entries": 5,
    "active_entries": 5,
    "total_hits": 12,
    "ttl_minutes": 60
  }
}
```

---

### Roadmap Generation

#### POST /api/roadmaps/generate

Generate a career roadmap based on resume and target jobs.

**Rate Limit:** 10 requests/minute, 100 requests/hour per IP

**Request Body:**
```json
{
  "resume_text": "Software Engineer with 5 years experience in Python...",
  "target_jobs": ["Senior DevOps Engineer", "Cloud Architect"],
  "user_id": "optional-user-id"
}
```

**Validation:**
- `resume_text`: 50-50000 characters
- `target_jobs`: 1-3 job titles, each 3-200 characters
- `user_id`: Optional, max 100 characters

**Response:**
```json
{
  "nodes": [
    {
      "id": "skill-1",
      "type": "default",
      "data": { "label": "Docker" },
      "position": { "x": 100, "y": 100 },
      "style": { "background": "#ff6b6b" }
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "source": "start",
      "target": "skill-1",
      "animated": true
    }
  ],
  "milestones": [
    {
      "title": "Foundation Skills",
      "skills": ["Docker", "Kubernetes"],
      "timeframe": "Months 1-3"
    }
  ],
  "skill_gaps": [
    {
      "skill": "Docker",
      "priority": "high",
      "difficulty": "medium",
      "estimated_hours": 60
    }
  ],
  "courses": [
    {
      "skill": "Docker",
      "title": "Docker Mastery",
      "provider": "Udemy",
      "url": "https://..."
    }
  ],
  "projects": [
    {
      "skill": "Docker",
      "title": "Containerize a web application",
      "description": "..."
    }
  ],
  "certifications": [
    {
      "skill": "AWS",
      "name": "AWS Solutions Architect",
      "provider": "AWS"
    }
  ]
}
```

**Error Responses:**
- `422`: Validation error (invalid input)
- `429`: Rate limit exceeded
- `500`: Server error

---

### Progress Tracking

#### POST /api/roadmaps/{roadmap_id}/progress

Initialize progress tracking for a roadmap.

**Request Body:**
```json
["Python", "AWS", "Docker", "Kubernetes"]
```

**Response:**
```json
{
  "roadmap_id": "roadmap-123",
  "created_at": "2026-02-19T16:30:00Z",
  "total_skills": 4
}
```

---

#### GET /api/roadmaps/{roadmap_id}/progress

Get progress for a roadmap.

**Response:**
```json
{
  "roadmap_id": "roadmap-123",
  "completion_percentage": 50.0,
  "statistics": {
    "not_started": 1,
    "in_progress": 1,
    "completed": 2
  },
  "skills": {
    "Python": {
      "status": "completed",
      "started_at": "2026-02-19T10:00:00Z",
      "completed_at": "2026-02-19T15:00:00Z",
      "notes": "Finished Python course"
    },
    "AWS": {
      "status": "in_progress",
      "started_at": "2026-02-19T14:00:00Z",
      "completed_at": null,
      "notes": "Working on AWS certification"
    }
  },
  "updated_at": "2026-02-19T16:30:00Z"
}
```

---

#### PATCH /api/roadmaps/{roadmap_id}/skills/{skill}

Update progress for a specific skill.

**Request Body:**
```json
{
  "skill": "Python",
  "status": "completed",
  "notes": "Finished Python course"
}
```

**Status Values:**
- `not_started`
- `in_progress`
- `completed`

**Response:**
```json
{
  "skill": "Python",
  "status": "completed",
  "started_at": "2026-02-19T10:00:00Z",
  "completed_at": "2026-02-19T15:00:00Z",
  "notes": "Finished Python course",
  "roadmap_completion": 50.0
}
```

---

### Career Path Comparison

#### POST /api/compare-paths

Compare two career paths side-by-side.

**Request Body:**
```json
{
  "current_skills": ["Python", "Git", "Docker"],
  "path1_skills": ["Python", "AWS", "Docker", "Kubernetes"],
  "path2_skills": ["Python", "Azure", "Docker", "Terraform"],
  "path1_name": "AWS DevOps Engineer",
  "path2_name": "Azure DevOps Engineer"
}
```

**Response:**
```json
{
  "paths": {
    "AWS DevOps Engineer": {
      "total_skills": 4,
      "current_skills": 2,
      "missing_skills": 2,
      "readiness_percentage": 50.0,
      "gaps": ["aws", "kubernetes"],
      "unique_gaps": ["aws", "kubernetes"],
      "learning_effort": {
        "total_skills": 2,
        "estimated_hours": 120,
        "estimated_weeks": 12,
        "difficulty_breakdown": {
          "easy": 0,
          "medium": 1,
          "hard": 1
        },
        "average_hours_per_skill": 60.0
      }
    },
    "Azure DevOps Engineer": {
      "total_skills": 4,
      "current_skills": 2,
      "missing_skills": 2,
      "readiness_percentage": 50.0,
      "gaps": ["azure", "terraform"],
      "unique_gaps": ["azure", "terraform"],
      "learning_effort": {
        "total_skills": 2,
        "estimated_hours": 120,
        "estimated_weeks": 12,
        "difficulty_breakdown": {
          "easy": 0,
          "medium": 2,
          "hard": 0
        },
        "average_hours_per_skill": 60.0
      }
    }
  },
  "common_gaps": [],
  "recommendation": {
    "easier_path": "Equal difficulty",
    "gap_difference": 0,
    "should_learn_first": []
  }
}
```

---

### Cache Management

#### POST /api/cache/clear

Clear all cached responses.

**Response:**
```json
{
  "message": "Cache cleared",
  "stats": {
    "total_entries": 0,
    "active_entries": 0,
    "total_hits": 0,
    "ttl_minutes": 60
  }
}
```

---

#### POST /api/cache/cleanup

Remove expired cache entries.

**Response:**
```json
{
  "message": "Removed 3 expired entries",
  "removed": 3,
  "stats": {
    "total_entries": 5,
    "active_entries": 5,
    "total_hits": 12,
    "ttl_minutes": 60
  }
}
```

---

### Rate Limiting

#### GET /api/rate-limit/stats

Get rate limit statistics for current IP.

**Response:**
```json
{
  "requests_last_minute": 3,
  "requests_last_hour": 15,
  "minute_limit": 10,
  "hour_limit": 100,
  "minute_remaining": 7,
  "hour_remaining": 85
}
```

---

## Rate Limits

All endpoints are subject to rate limiting:

- **Per Minute:** 10 requests
- **Per Hour:** 100 requests

Rate limits are tracked per IP address.

**Rate Limit Headers:**
- When rate limit is exceeded, API returns `429 Too Many Requests`
- Error message includes which limit was exceeded

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request format"
}
```

### 404 Not Found
```json
{
  "detail": "Progress not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "resume_text"],
      "msg": "ensure this value has at least 50 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded: 10 requests per minute"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Workflow not initialized"
}
```

---

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

---

## CORS

CORS is enabled for all origins in development. Configure appropriately for production.

---

## Authentication

Currently no authentication is required. Future versions will include:
- AWS Cognito integration
- JWT token authentication
- User-specific roadmaps and progress

---

## Best Practices

1. **Cache Responses:** Identical requests within 60 minutes return cached results
2. **Rate Limiting:** Stay within rate limits to avoid 429 errors
3. **Input Validation:** Validate inputs client-side before sending
4. **Error Handling:** Handle all error responses appropriately
5. **Progress Tracking:** Initialize progress before updating skills

---

## Example Workflows

### Generate and Track Roadmap

```bash
# 1. Generate roadmap
curl -X POST http://localhost:8000/api/roadmaps/generate \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Software Engineer with Python experience...",
    "target_jobs": ["Senior DevOps Engineer"]
  }'

# 2. Initialize progress tracking
curl -X POST http://localhost:8000/api/roadmaps/roadmap-123/progress \
  -H "Content-Type: application/json" \
  -d '["Docker", "Kubernetes", "AWS"]'

# 3. Update skill progress
curl -X PATCH http://localhost:8000/api/roadmaps/roadmap-123/skills/Docker \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "Docker",
    "status": "completed",
    "notes": "Completed Docker course"
  }'

# 4. Check progress
curl http://localhost:8000/api/roadmaps/roadmap-123/progress
```

### Compare Career Paths

```bash
curl -X POST http://localhost:8000/api/compare-paths \
  -H "Content-Type: application/json" \
  -d '{
    "current_skills": ["Python", "Git"],
    "path1_skills": ["Python", "AWS", "Docker"],
    "path2_skills": ["Python", "Azure", "Kubernetes"],
    "path1_name": "AWS Path",
    "path2_name": "Azure Path"
  }'
```

---

## Support

For issues or questions:
- GitHub: https://github.com/jfowler-cloud/career-path-architect
- Documentation: See README.md
