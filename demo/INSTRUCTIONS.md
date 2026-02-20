# Demo Instructions for Career Path Architect

## How to Use the Demo

### 1. Start the Application
```bash
cd ~/Desktop/Projects/career-path-architect
./dev.sh
```

Then open http://localhost:3000

### 2. Load the Sample Resume

Copy and paste the content from `sample-resume.txt` into the resume text area.

**Profile Summary:**
- Mid-level engineer (6 years experience)
- Strong in React, Node.js, PostgreSQL
- Basic AWS knowledge (Cloud Practitioner)
- Limited experience with advanced cloud services

### 3. Target Job Titles to Try

Choose ONE of these target roles to see different career paths:

#### Option 1: Senior Cloud Architect (Big Jump)
**Target Job:** `Senior Cloud Architect`

**What to expect:**
- Large skill gaps in AWS services (Lambda, ECS, CloudFormation, etc.)
- Need for advanced certifications (Solutions Architect Professional)
- Infrastructure as Code skills (Terraform, CDK)
- High priority items: AWS architecture patterns, multi-region design
- Timeline: 12-18 months of focused learning

#### Option 2: Full Stack Tech Lead (Natural Progression)
**Target Job:** `Full Stack Tech Lead`

**What to expect:**
- Moderate gaps in leadership and system design
- Need for advanced architecture patterns
- Team management and mentoring skills
- Medium priority items: Microservices, CI/CD, monitoring
- Timeline: 6-9 months

#### Option 3: DevOps Engineer (Career Pivot)
**Target Job:** `DevOps Engineer`

**What to expect:**
- Significant gaps in infrastructure and automation
- Need for Kubernetes, Terraform, CI/CD pipelines
- Monitoring and observability tools (Prometheus, Grafana)
- High priority items: Container orchestration, IaC
- Timeline: 9-12 months

#### Option 4: Staff Software Engineer (Senior IC Track)
**Target Job:** `Staff Software Engineer`

**What to expect:**
- Gaps in system design and architecture
- Need for distributed systems knowledge
- Performance optimization and scalability
- Medium priority items: Design patterns, scalability
- Timeline: 8-12 months

### 4. Understanding the Results

#### Visual Roadmap
- **Red nodes** = High priority (hard skills, very important)
- **Yellow nodes** = Medium priority (moderate difficulty)
- **Green nodes** = Low priority (easier, quick wins)

#### Skill Gaps Section
Shows missing skills with:
- Priority level (high/medium/low)
- Importance rating
- Difficulty rating
- Estimated learning time

#### Recommendations
- **Courses**: Specific online courses to take
- **Projects**: Hands-on projects to build the skills
- **Certifications**: Industry certifications to pursue

### 5. Best Demo Flow

1. **Start with Option 2** (Full Stack Tech Lead) - Shows natural progression
2. **Then try Option 1** (Senior Cloud Architect) - Shows major career pivot
3. **Compare the roadmaps** - See how different the paths are

### 6. Testing Multiple Targets

You can also enter multiple job titles separated by commas:
```
Full Stack Tech Lead, Senior Cloud Architect
```

This will analyze gaps for both roles and create a combined roadmap.

### 7. Expected Generation Time

- Resume analysis: ~5-10 seconds
- Job parsing: ~5-10 seconds
- Gap analysis: ~5-10 seconds
- Learning path design: ~10-15 seconds
- Roadmap generation: ~5-10 seconds

**Total: 30-60 seconds**

### 8. Troubleshooting

**If you get an error:**
- Check that AWS credentials are configured (`aws configure`)
- Verify you have Bedrock access to Claude Opus 4.5
- Check backend logs for detailed error messages

**If the roadmap looks empty:**
- The AI might have found no significant gaps
- Try a more senior or different role
- Check the console for any errors

### 9. What Makes a Good Demo

**Good combinations:**
- Current: Mid-level → Target: Senior (shows growth path)
- Current: Frontend → Target: Full Stack (shows skill expansion)
- Current: Developer → Target: Architect (shows career pivot)

**Less interesting:**
- Current: Senior → Target: Junior (downgrade)
- Current: Full Stack → Target: Frontend (narrowing)

---

## Sample Target Jobs by Career Path

### Cloud/Infrastructure Track
- Cloud Solutions Architect
- Senior DevOps Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)

### Engineering Leadership Track
- Engineering Manager
- Technical Lead
- Staff Software Engineer
- Principal Engineer

### Specialized Technical Track
- Machine Learning Engineer
- Security Engineer
- Data Engineer
- Backend Architect

---

## Tips for Best Results

1. **Be specific with job titles** - "Senior Cloud Architect" is better than "Architect"
2. **Use industry-standard titles** - Titles that appear on job boards
3. **One target at a time** - Easier to understand the roadmap
4. **Try different seniority levels** - See how the gaps change

---

**Enjoy exploring your career path! 🚀**
