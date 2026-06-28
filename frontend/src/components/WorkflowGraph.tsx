import { useEffect } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  useNodesState,
  useEdgesState,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { fetchWorkflow } from "../lib/api";

interface WorkflowGraphProps {
  activeAgent: string;
}

export function WorkflowGraph({ activeAgent }: WorkflowGraphProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  useEffect(() => {
    fetchWorkflow().then((data) => {
      const flowNodes: Node[] = data.nodes.map((n) => ({
        id: n.id,
        data: { label: n.label },
        position: { x: n.position.x / 4, y: n.position.y + (n.id === activeAgent ? -10 : 0) },
        style: {
          background: n.id === activeAgent ? "#0369a1" : "#1f2937",
          color: "#f9fafb",
          border: n.id === activeAgent ? "2px solid #0ea5e9" : "1px solid #374151",
          borderRadius: 8,
          fontSize: 11,
          padding: "4px 8px",
          width: 120,
        },
      }));
      const flowEdges: Edge[] = data.edges.map((e, i) => ({
        id: `e${i}`,
        source: e.source,
        target: e.target,
        animated: e.target === activeAgent,
        style: { stroke: "#4b5563" },
      }));
      setNodes(flowNodes);
      setEdges(flowEdges);
    });
  }, [activeAgent, setNodes, setEdges]);

  return (
    <div className="h-48 rounded-lg border border-gray-700 overflow-hidden">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        proOptions={{ hideAttribution: true }}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        panOnScroll
      >
        <Background color="#374151" gap={16} />
        <Controls showInteractive={false} />
        <MiniMap nodeColor="#0369a1" maskColor="rgba(0,0,0,0.6)" />
      </ReactFlow>
    </div>
  );
}
