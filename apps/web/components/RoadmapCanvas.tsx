"use client";

import { useEffect, memo } from "react";
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
} from "@xyflow/react";
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
      </ReactFlow>
    </div>
  );
});

export default RoadmapCanvas;
