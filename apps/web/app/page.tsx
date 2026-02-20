"use client";

import { useState } from "react";
import AppLayout from "@cloudscape-design/components/app-layout";
import TopNavigation from "@cloudscape-design/components/top-navigation";
import Container from "@cloudscape-design/components/container";
import Header from "@cloudscape-design/components/header";
import SpaceBetween from "@cloudscape-design/components/space-between";
import Button from "@cloudscape-design/components/button";
import Textarea from "@cloudscape-design/components/textarea";
import Input from "@cloudscape-design/components/input";
import Alert from "@cloudscape-design/components/alert";

import RoadmapCanvas from "@/components/RoadmapCanvas";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const EXAMPLE_RESUME = `Senior Software Engineer with 5 years of experience in full-stack development.

Skills:
- Python, JavaScript, TypeScript
- React, Node.js, FastAPI
- AWS (EC2, S3, Lambda)
- Docker, Kubernetes
- PostgreSQL, MongoDB

Experience:
- Built scalable web applications serving 100K+ users
- Implemented CI/CD pipelines with GitHub Actions
- Led team of 3 developers on microservices project
- Reduced API response time by 40% through optimization

Education:
- BS Computer Science, State University
`;

export default function Home() {
  const [resumeText, setResumeText] = useState("");
  const [targetJob, setTargetJob] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [specialtyInfo, setSpecialtyInfo] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [roadmapData, setRoadmapData] = useState<any>(null);

  const loadExample = () => {
    setResumeText(EXAMPLE_RESUME);
    setTargetJob("Senior Cloud Architect");
    setJobDescription("");
    setSpecialtyInfo("");
    setError("");
  };

  const handleGenerate = async () => {
    if (!resumeText || !targetJob) {
      setError("Please provide both resume and target job");
      return;
    }

    if (resumeText.length < 50) {
      setError("Resume must be at least 50 characters");
      return;
    }

    setLoading(true);
    setError("");
    setRoadmapData(null); // Clear previous results

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000); // 60s timeout

      const response = await fetch(`${API_URL}/api/roadmaps/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          resume_text: resumeText,
          target_jobs: [targetJob],
          job_description: jobDescription || undefined,
          specialty_info: specialtyInfo || undefined,
          user_id: "demo"
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "Failed to generate roadmap" }));
        throw new Error(errorData.detail || "Failed to generate roadmap");
      }

      const data = await response.json();
      setRoadmapData(data);
    } catch (err: any) {
      if (err.name === 'AbortError') {
        setError("Request timed out. Please try again.");
      } else {
        setError(err.message || "An error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <TopNavigation
        identity={{
          href: "/",
          title: "Career Path Architect",
        }}
        utilities={[
          {
            type: "button",
            text: "GitHub",
            href: "https://github.com/jfowler-cloud/career-path-architect",
            external: true,
          },
        ]}
      />
      <AppLayout
        navigationHide
        toolsHide
        content={
          <SpaceBetween size="l">
            <Container
              header={
                <Header variant="h2" description="Generate your personalized career roadmap">
                  Create Career Roadmap
                </Header>
              }
            >
              <SpaceBetween size="m">
                {error && <Alert type="error">{error}</Alert>}
                
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <strong>Try it out:</strong>
                  </div>
                  <Button onClick={loadExample} variant="link">
                    Load Example Resume
                  </Button>
                </div>

                <Textarea
                  label="Resume"
                  placeholder="Paste your resume here..."
                  value={resumeText}
                  onChange={({ detail }) => setResumeText(detail.value)}
                  rows={10}
                />

                <Input
                  label="Target Job Title"
                  placeholder="e.g., Senior Cloud Architect"
                  value={targetJob}
                  onChange={({ detail }) => setTargetJob(detail.value)}
                />

                <Textarea
                  label="Job Description (Optional)"
                  description="Paste the full job posting for more accurate gap analysis"
                  placeholder="Paste job description here for detailed requirements analysis..."
                  value={jobDescription}
                  onChange={({ detail }) => setJobDescription(detail.value)}
                  rows={6}
                />

                <Textarea
                  label="Additional Context (Optional)"
                  description="Any specific areas of focus, career goals, or constraints"
                  placeholder="e.g., Focus on cloud-native technologies, interested in leadership track, prefer remote-friendly skills..."
                  value={specialtyInfo}
                  onChange={({ detail }) => setSpecialtyInfo(detail.value)}
                  rows={3}
                />

                <Button
                  variant="primary"
                  onClick={handleGenerate}
                  loading={loading}
                  disabled={!resumeText || !targetJob}
                  loadingText="Generating roadmap..."
                >
                  Generate Roadmap
                </Button>
                
                {loading && (
                  <Alert type="info">
                    This may take 30-60 seconds. AI is analyzing your resume and generating recommendations...
                  </Alert>
                )}
              </SpaceBetween>
            </Container>

            {roadmapData && (
              <>
                <Container
                  header={
                    <Header 
                      variant="h2"
                      description={`${roadmapData.fit_score}% match • ${roadmapData.matched_skills?.length || 0} skills matched • ${roadmapData.skill_gaps?.length || 0} gaps identified`}
                    >
                      Career Readiness Assessment
                    </Header>
                  }
                >
                  <SpaceBetween size="m">
                    {roadmapData.critical_review && (
                      <div>
                        <div style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
                          <div>
                            <strong>Overall Rating:</strong> {roadmapData.critical_review.overallRating}/10
                          </div>
                          <div>
                            <strong>Readiness:</strong> {roadmapData.critical_review.readinessLevel}
                          </div>
                        </div>
                        
                        {roadmapData.critical_review.summary && (
                          <Alert type="info" style={{marginTop: "16px"}}>
                            {roadmapData.critical_review.summary}
                          </Alert>
                        )}

                        {roadmapData.critical_review.strengths?.length > 0 && (
                          <div style={{marginTop: "16px"}}>
                            <strong>✅ Strengths:</strong>
                            <ul style={{marginTop: "8px"}}>
                              {roadmapData.critical_review.strengths.map((s: string, i: number) => (
                                <li key={`strength-${i}`}>{s}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {roadmapData.critical_review.weaknesses?.length > 0 && (
                          <div style={{marginTop: "16px"}}>
                            <strong>⚠️ Areas for Improvement:</strong>
                            <ul style={{marginTop: "8px"}}>
                              {roadmapData.critical_review.weaknesses.map((w: string, i: number) => (
                                <li key={`weakness-${i}`}>{w}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {roadmapData.critical_review.actionableSteps?.length > 0 && (
                          <div style={{marginTop: "16px"}}>
                            <strong>🎯 Action Steps:</strong>
                            <ol style={{marginTop: "8px"}}>
                              {roadmapData.critical_review.actionableSteps.map((step: string, i: number) => (
                                <li key={`action-${i}`}>{step}</li>
                              ))}
                            </ol>
                          </div>
                        )}
                      </div>
                    )}
                  </SpaceBetween>
                </Container>

                <Container
                  header={<Header variant="h2">Visual Roadmap</Header>}
                >
                  <RoadmapCanvas
                    nodes={roadmapData.nodes}
                    edges={roadmapData.edges}
                  />
                </Container>

                {roadmapData.skill_gaps.length > 0 && (
                  <Container
                    header={
                      <Header 
                        variant="h2"
                        info={<span>Skills you need to develop for this role</span>}
                      >
                        Skill Gaps ({roadmapData.skill_gaps.length})
                      </Header>
                    }
                  >
                    <SpaceBetween size="xs">
                      {roadmapData.skill_gaps.map((gap: any, i: number) => (
                        <div key={`gap-${i}-${gap.skill}`} style={{
                          padding: "8px",
                          background: gap.priority === "high" ? "#fff3e0" : "#f3e5f5",
                          borderRadius: "4px"
                        }}>
                          <strong>{gap.skill}</strong> - {gap.priority} priority ({gap.time_months} months)
                        </div>
                      ))}
                    </SpaceBetween>
                  </Container>
                )}

                {roadmapData.courses.length > 0 && (
                  <Container
                    header={
                      <Header 
                        variant="h2"
                        description="Recommended online courses to build missing skills"
                      >
                        Recommended Courses ({roadmapData.courses.length})
                      </Header>
                    }
                  >
                    <SpaceBetween size="s">
                      {roadmapData.courses.map((course: any, i: number) => (
                        <div key={`course-${i}-${course.name}`} style={{padding: "12px", background: "#f5f5f5", borderRadius: "4px"}}>
                          <div><strong>{course.name}</strong></div>
                          <div style={{color: "#666"}}>{course.provider} • {course.duration}</div>
                          {course.url && (
                            <div style={{marginTop: "4px"}}>
                              <a href={course.url} target="_blank" rel="noopener noreferrer" style={{color: "#0073bb"}}>
                                View Course →
                              </a>
                            </div>
                          )}
                        </div>
                      ))}
                    </SpaceBetween>
                  </Container>
                )}

                {roadmapData.projects.length > 0 && (
                  <Container
                    header={
                      <Header 
                        variant="h2"
                        description="Hands-on projects to practice and demonstrate skills"
                      >
                        Project Ideas ({roadmapData.projects.length})
                      </Header>
                    }
                  >
                    <SpaceBetween size="s">
                      {roadmapData.projects.map((project: any, i: number) => (
                        <div key={`project-${i}-${project.name}`} style={{padding: "12px", background: "#f5f5f5", borderRadius: "4px"}}>
                          <div><strong>{project.name}</strong></div>
                          <div style={{marginTop: "4px"}}>{project.description}</div>
                          {project.skills && (
                            <div style={{marginTop: "8px", color: "#666", fontSize: "0.9em"}}>
                              Skills: {project.skills.join(", ")}
                            </div>
                          )}
                        </div>
                      ))}
                    </SpaceBetween>
                  </Container>
                )}
              </>
            )}
          </SpaceBetween>
        }
      />
    </>
  );
}
