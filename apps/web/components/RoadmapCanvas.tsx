"use client";

import { useEffect, memo, useCallback } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  useNodesState,
  useEdgesState,
  BackgroundVariant,
  Panel,
} from "@xyflow/react";
import { toPng } from "html-to-image";
import "@xyflow/react/dist/style.css";

interface RoadmapCanvasProps {
  nodes: Node[];
  edges: Edge[];
}

const RoadmapCanvas = memo(function RoadmapCanvas({ nodes, edges }: RoadmapCanvasProps) {
  const [nodesState, setNodes, onNodesChange] = useNodesState(nodes);
  const [edgesState, setEdges, onEdgesChange] = useEdgesState(edges);

  useEffect(() => {
    setNodes(nodes);
  }, [nodes, setNodes]);

  useEffect(() => {
    setEdges(edges);
  }, [edges, setEdges]);

  const downloadImage = useCallback(() => {
    const viewport = document.querySelector('.react-flow__viewport') as HTMLElement;
    if (!viewport) return;

    toPng(viewport, {
      backgroundColor: '#ffffff',
      width: viewport.offsetWidth,
      height: viewport.offsetHeight,
    })
      .then((dataUrl) => {
        const a = document.createElement('a');
        a.setAttribute('download', 'career-roadmap.png');
        a.setAttribute('href', dataUrl);
        a.click();
      })
      .catch((err) => {
        console.error('Failed to export image:', err);
      });
  }, []);

  const downloadJSON = useCallback(() => {
    const data = {
      nodes: nodesState,
      edges: edgesState,
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('download', 'career-roadmap.json');
    a.setAttribute('href', url);
    a.click();
    URL.revokeObjectURL(url);
  }, [nodesState, edgesState]);

  return (
    <div style={{ width: "100%", height: "600px", border: "1px solid #ddd", borderRadius: "8px" }}>
      <ReactFlow
        nodes={nodesState}
        edges={edgesState}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        minZoom={0.5}
        maxZoom={1.5}
      >
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
        <Controls />
        <MiniMap zoomable pannable />
        <Panel position="top-right" style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={downloadImage}
            style={{
              padding: '8px 16px',
              backgroundColor: '#0073bb',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '14px',
            }}
          >
            📥 Export PNG
          </button>
          <button
            onClick={downloadJSON}
            style={{
              padding: '8px 16px',
              backgroundColor: '#16191f',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '14px',
            }}
          >
            💾 Export JSON
          </button>
        </Panel>
      </ReactFlow>
    </div>
  );
});

export default RoadmapCanvas;
