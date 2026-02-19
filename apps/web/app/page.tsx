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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [roadmapData, setRoadmapData] = useState<any>(null);

  const loadExample = () => {
    setResumeText(EXAMPLE_RESUME);
    setTargetJob("Senior Cloud Architect");
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
                  header={<Header variant="h2">Visual Roadmap</Header>}
                >
                  <RoadmapCanvas
                    nodes={roadmapData.nodes}
                    edges={roadmapData.edges}
                  />
                </Container>

                <Container
                  header={<Header variant="h2">Skill Gaps</Header>}
                >
                  {roadmapData.skill_gaps.length > 0 ? (
                    <SpaceBetween size="xs">
                      {roadmapData.skill_gaps.map((gap: any, i: number) => (
                        <div key={i}>
                          <strong>{gap.skill}</strong> - {gap.priority} priority ({gap.time_months} months)
                        </div>
                      ))}
                    </SpaceBetween>
                  ) : (
                    <div>No skill gaps identified! You're well-matched for this role.</div>
                  )}
                </Container>

                <Container
                  header={<Header variant="h2">Recommended Courses</Header>}
                >
                  {roadmapData.courses.length > 0 ? (
                    <SpaceBetween size="xs">
                      {roadmapData.courses.map((course: any, i: number) => (
                        <div key={i}>
                          <strong>{course.name}</strong> - {course.provider} ({course.duration})
                          {course.url && <div><a href={course.url} target="_blank" rel="noopener noreferrer">View Course</a></div>}
                        </div>
                      ))}
                    </SpaceBetween>
                  ) : (
                    <div>No course recommendations available.</div>
                  )}
                </Container>

                <Container
                  header={<Header variant="h2">Project Ideas</Header>}
                >
                  {roadmapData.projects.length > 0 ? (
                    <SpaceBetween size="xs">
                      {roadmapData.projects.map((project: any, i: number) => (
                        <div key={i}>
                          <strong>{project.name}</strong>
                          <p>{project.description}</p>
                          {project.skills && <div><em>Skills: {project.skills.join(", ")}</em></div>}
                        </div>
                      ))}
                    </SpaceBetween>
                  ) : (
                    <div>No project recommendations available.</div>
                  )}
                </Container>
              </>
            )}
          </SpaceBetween>
        }
      />
    </>
  );
}
