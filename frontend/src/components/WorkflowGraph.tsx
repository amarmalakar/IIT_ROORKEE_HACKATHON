import { useEffect, useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  Node,
  Edge,
  useNodesState,
  useEdgesState,
  MarkerType,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { fetchWorkflow } from "../lib/api";

interface WorkflowGraphProps {
  activeAgent: string;
}

const NODE_WIDTH = 108;
const NODE_HEIGHT = 40;
const GAP_X = 28;
const GAP_Y = 56;
const NODES_PER_ROW = 7;

/** Compute a 2-row grid so 13 agents don't overlap in the canvas. */
function layoutNodes(
  nodes: Array<{ id: string; label: string }>,
  activeAgent: string
): Node[] {
  return nodes.map((n, i) => {
    const row = Math.floor(i / NODES_PER_ROW);
    const col = i % NODES_PER_ROW;
    const isActive = n.id === activeAgent;

    return {
      id: n.id,
      data: { label: n.label },
      position: {
        x: col * (NODE_WIDTH + GAP_X),
        y: row * (NODE_HEIGHT + GAP_Y),
      },
      style: {
        background: isActive ? "#0369a1" : "#1f2937",
        color: "#f9fafb",
        border: isActive ? "2px solid #38bdf8" : "1px solid #4b5563",
        borderRadius: 8,
        fontSize: 10,
        fontWeight: 500,
        padding: "6px 8px",
        width: NODE_WIDTH,
        height: NODE_HEIGHT,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center" as const,
        lineHeight: 1.2,
        boxShadow: isActive ? "0 0 12px rgba(14,165,233,0.45)" : "none",
      },
    };
  });
}

function buildEdges(
  edges: Array<{ source: string; target: string; label?: string }>,
  activeAgent: string
): Edge[] {
  return edges.map((e, i) => {
    const isLoop = e.label === "retry" || e.source === "evaluator";
    const isActive =
      e.target === activeAgent || (isLoop && activeAgent === "language_specialist");

    return {
      id: `e${i}`,
      source: e.source,
      target: e.target,
      label: isLoop ? "retry" : undefined,
      animated: isActive,
      type: isLoop ? "smoothstep" : "default",
      style: {
        stroke: isLoop ? "#f59e0b" : "#6b7280",
        strokeWidth: isLoop ? 2 : 1.5,
      },
      labelStyle: { fill: "#fbbf24", fontSize: 9 },
      markerEnd: { type: MarkerType.ArrowClosed, color: isLoop ? "#f59e0b" : "#6b7280" },
    };
  });
}

export function WorkflowGraph({ activeAgent }: WorkflowGraphProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  const graphHeight = useMemo(() => {
    const rows = Math.ceil(13 / NODES_PER_ROW);
    return Math.max(200, rows * (NODE_HEIGHT + GAP_Y) + 48);
  }, []);

  useEffect(() => {
    fetchWorkflow().then((data) => {
      const flowNodes = layoutNodes(
        data.nodes.map((n) => ({ id: n.id, label: n.label })),
        activeAgent
      );
      const flowEdges = buildEdges(data.edges, activeAgent);
      setNodes(flowNodes);
      setEdges(flowEdges);
    });
  }, [activeAgent, setNodes, setEdges]);

  return (
    <div
      className="rounded-lg border border-gray-700 overflow-hidden bg-gray-900/50"
      style={{ height: graphHeight }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        fitViewOptions={{ padding: 0.2, minZoom: 0.5, maxZoom: 1.2 }}
        minZoom={0.4}
        maxZoom={1.5}
        proOptions={{ hideAttribution: true }}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        panOnScroll
        zoomOnScroll
      >
        <Background color="#374151" gap={20} size={1} />
        <Controls showInteractive={false} className="!bg-gray-800 !border-gray-600" />
      </ReactFlow>
    </div>
  );
}
