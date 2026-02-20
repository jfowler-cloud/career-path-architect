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

**Optional - Add Job Description:**
```
We're seeking a Senior Cloud Architect to design and implement scalable AWS solutions.

Requirements:
- 8+ years experience with AWS services (Lambda, ECS, CloudFormation, CDK)
- Expert in Infrastructure as Code (Terraform, CDK)
- Experience with multi-region architectures and disaster recovery
- Strong knowledge of security best practices and compliance
- AWS Solutions Architect Professional certification required
- Experience leading technical teams

Nice to have:
- Kubernetes and container orchestration
- CI/CD pipeline design
- Cost optimization strategies
```

**Optional - Add Specialty Info:**
```
Focus on serverless and container technologies. Interested in technical leadership path. Prefer remote-friendly skills.
```

**What to expect:**
- Fit Score: ~30-40% (significant gaps)
- Large skill gaps in AWS services (Lambda, ECS, CloudFormation, etc.)
- Critical Review: "Not ready" or "Somewhat ready"
- Need for advanced certifications (Solutions Architect Professional)
- Infrastructure as Code skills (Terraform, CDK)
- High priority items: AWS architecture patterns, multi-region design
- Timeline: 12-18 months of focused learning
- Matched Skills: Basic AWS (EC2, S3), Docker
- Missing Skills: Advanced AWS, IaC, multi-region, security

#### Option 2: Full Stack Tech Lead (Natural Progression)
**Target Job:** `Full Stack Tech Lead`

**Optional - Add Job Description:**
```
Looking for a Full Stack Tech Lead to guide our engineering team.

Requirements:
- 6+ years full-stack development experience
- Expert in React, Node.js, TypeScript
- Experience with system design and architecture
- Team leadership and mentoring experience
- Strong communication skills
- CI/CD and DevOps knowledge

Nice to have:
- Microservices architecture
- AWS or cloud platform experience
- Agile/Scrum leadership
```

**What to expect:**
- Fit Score: ~60-70% (good match)
- Moderate gaps in leadership and system design
- Critical Review: "Ready" or "Somewhat ready"
- Need for advanced architecture patterns
- Team management and mentoring skills
- Medium priority items: Microservices, CI/CD, monitoring
- Timeline: 6-9 months
- Matched Skills: React, Node.js, PostgreSQL, Docker
- Missing Skills: System design, team leadership, microservices

#### Option 3: DevOps Engineer (Career Pivot)
**Target Job:** `DevOps Engineer`

**What to expect:**
- Fit Score: ~40-50% (moderate gaps)
- Significant gaps in infrastructure and automation
- Critical Review: "Somewhat ready"
- Need for Kubernetes, Terraform, CI/CD pipelines
- Monitoring and observability tools (Prometheus, Grafana)
- High priority items: Container orchestration, IaC
- Timeline: 9-12 months
- Matched Skills: Docker, AWS basics, GitHub Actions
- Missing Skills: Kubernetes, Terraform, monitoring, IaC

#### Option 4: Staff Software Engineer (Senior IC Track)
**Target Job:** `Staff Software Engineer`

**What to expect:**
- Fit Score: ~50-60% (moderate match)
- Gaps in system design and architecture
- Critical Review: "Somewhat ready"
- Need for distributed systems knowledge
- Performance optimization and scalability
- Medium priority items: Design patterns, scalability
- Timeline: 8-12 months
- Matched Skills: Strong coding, some architecture
- Missing Skills: Distributed systems, advanced design patterns

### 4. Understanding the Results

#### Fit Score & Matched Skills (NEW!)
- **Fit Score**: 0-100% showing how well you match the role
- **Matched Skills**: List of skills you already have
- **Missing Skills**: What you need to learn

#### Critical Review Section (NEW!)
- **Overall Rating**: 1-10 score of career readiness
- **Readiness Level**: Not ready → Somewhat ready → Ready → Highly ready
- **Strengths**: What works well in your profile
- **Weaknesses**: Areas needing improvement
- **Action Steps**: Specific improvements to make
- **Competitive Analysis**: How you compare to typical candidates
- **Timeline Realism**: Honest assessment of learning timeline

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

**With TESTING mode (Haiku 3.0 - default):**
- Resume analysis: ~3-5 seconds
- Job parsing: ~3-5 seconds
- Gap analysis: ~2-3 seconds
- Learning path design: ~5-8 seconds
- Critical review: ~5-8 seconds
- Roadmap generation: ~2-3 seconds

**Total: 20-35 seconds** (much faster than PREMIUM!)

**With PREMIUM mode (Opus 4.5):**
- Total: 30-60 seconds (better quality, slower)

**Deployment Modes:**
- `TESTING` (default): Haiku 3.0 - Fast & cheap for development
- `OPTIMIZED`: Mix of models - Balanced cost/quality
- `PREMIUM`: Opus 4.5 - Best quality, highest cost

Set via environment variable:
```bash
export DEPLOYMENT_MODE=TESTING  # or OPTIMIZED or PREMIUM
```

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
- Current: Mid-level → Target: Senior (shows growth path with fit score)
- Current: Frontend → Target: Full Stack (shows skill expansion)
- Current: Developer → Target: Architect (shows career pivot with honest assessment)

**Try with job description:**
- Paste actual job posting for more accurate gap analysis
- See how fit score changes with detailed requirements
- Get specific skill matches vs generic recommendations

**Try with specialty info:**
- "Focus on serverless technologies" → Get AWS Lambda, Step Functions recommendations
- "Interested in leadership track" → Get team management, communication skills
- "Prefer remote-friendly skills" → Get async communication, documentation focus

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
3. **Add job description for accuracy** - Paste actual job posting for precise gap analysis
4. **Use specialty info for focus** - Guide recommendations to your interests
5. **One target at a time** - Easier to understand the roadmap
6. **Try different seniority levels** - See how fit score and gaps change
7. **Check critical review** - Honest assessment of readiness and timeline
8. **Review matched skills** - See what you already have going for you

---

**New Features Demonstrated:**
- ✅ Fit Score (0-100%) based on skill matching
- ✅ Matched Skills list showing current strengths
- ✅ Critical Review with honest assessment
- ✅ Job Description parsing for accurate requirements
- ✅ Specialty Info for focused recommendations
- ✅ Deployment modes (TESTING/OPTIMIZED/PREMIUM)

---

**Enjoy exploring your career path! 🚀**
