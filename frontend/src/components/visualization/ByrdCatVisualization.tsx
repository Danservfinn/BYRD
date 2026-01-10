/**
 * BYRD Cat Consciousness Visualization
 *
 * Simple procedural cat based on the archived byrd-cat-visualization.html
 * Uses basic shapes (spheres) without requiring external GLTF models
 */

import { Suspense, useRef, useMemo, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

// RSI phase colors for eye glow
const RSI_PHASE_COLORS: Record<string, string> = {
  idle: '#64748b',       // Gray
  reflect: '#8b5cf6',    // Purple
  verify: '#6366f1',     // Indigo
  collapse: '#ec4899',   // Pink
  route: '#f59e0b',      // Amber
  practice: '#10b981',   // Emerald
  record: '#3b82f6',     // Blue
  crystallize: '#06b6d4', // Cyan
  measure: '#84cc16',    // Lime
};

// System state to eye intensity mapping
const getEyeIntensity = (systemState: string, rsiPhase: string): number => {
  if (systemState === 'stopped' || systemState === 'idle') return 0.4;
  if (rsiPhase === 'collapse') return 1.2;
  if (systemState === 'running') return 0.8;
  return 0.6;
};

interface CatModelProps {
  rsiPhase: string;
  systemState: string;
}

// Procedural cat based on archived byrd-cat-visualization.html fallback
function ProceduralCat({ rsiPhase, systemState }: CatModelProps) {
  const catRef = useRef<THREE.Group>(null);
  const leftEyeRef = useRef<THREE.Mesh>(null);
  const rightEyeRef = useRef<THREE.Mesh>(null);

  const eyeColor = RSI_PHASE_COLORS[rsiPhase] || RSI_PHASE_COLORS.idle;
  const targetGlow = getEyeIntensity(systemState, rsiPhase);

  // Animation loop
  useFrame((state) => {
    if (!catRef.current) return;

    const elapsed = state.clock.getElapsedTime();

    // Breathing animation (matching archived version)
    const breathSpeed = systemState === 'dreaming' ? 0.3 : 0.5;
    const breathAmount = systemState === 'dreaming' ? 0.02 : 0.015;
    const breathPhase = Math.sin(elapsed * breathSpeed * Math.PI * 2);

    // Apply breathing to the cat
    catRef.current.scale.y = 1 + breathPhase * breathAmount;
    catRef.current.scale.x = 1 + breathPhase * breathAmount * 0.3;

    // Subtle idle sway (matching archived version)
    const idlePhase = elapsed * 0.3;
    catRef.current.rotation.y = Math.sin(idlePhase) * 0.02;
    catRef.current.rotation.z = Math.sin(idlePhase * 0.7) * 0.008;

    // Eye glow pulse (matching archived version)
    const glowPulse = targetGlow + Math.sin(elapsed * 0.5) * 0.2;

    [leftEyeRef.current, rightEyeRef.current].forEach((eye) => {
      if (eye && eye.material) {
        const mat = eye.material as THREE.MeshStandardMaterial;
        mat.emissiveIntensity = glowPulse;
      }
    });
  });

  return (
    <group ref={catRef} position={[0, 1, 0]}>
      {/* Body - oblate spheroid (chonky cat) */}
      <mesh scale={[1.2, 0.8, 1.5]} position={[0, 0.4, 0]} castShadow receiveShadow>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshStandardMaterial color="#0a0a0a" roughness={0.85} metalness={0.05} />
      </mesh>

      {/* Head */}
      <mesh position={[0, 0.7, 0.5]} castShadow receiveShadow>
        <sphereGeometry args={[0.3, 32, 32]} />
        <meshStandardMaterial color="#0a0a0a" roughness={0.85} metalness={0.05} />
      </mesh>

      {/* Left eye - gold glowing */}
      <mesh ref={leftEyeRef} position={[-0.1, 0.75, 0.75]} castShadow>
        <sphereGeometry args={[0.06, 16, 16]} />
        <meshStandardMaterial
          color={eyeColor}
          emissive={eyeColor}
          emissiveIntensity={0.6}
          roughness={0.2}
          metalness={0.3}
        />
      </mesh>

      {/* Right eye - gold glowing */}
      <mesh ref={rightEyeRef} position={[0.1, 0.75, 0.75]} castShadow>
        <sphereGeometry args={[0.06, 16, 16]} />
        <meshStandardMaterial
          color={eyeColor}
          emissive={eyeColor}
          emissiveIntensity={0.6}
          roughness={0.2}
          metalness={0.3}
        />
      </mesh>

      {/* Ears - subtle cones */}
      <mesh position={[-0.12, 0.95, 0.45]} rotation={[0.3, 0, -0.2]} castShadow>
        <coneGeometry args={[0.08, 0.2, 4]} />
        <meshStandardMaterial color="#0a0a0a" roughness={0.85} />
      </mesh>
      <mesh position={[0.12, 0.95, 0.45]} rotation={[0.3, 0, 0.2]} castShadow>
        <coneGeometry args={[0.08, 0.2, 4]} />
        <meshStandardMaterial color="#0a0a0a" roughness={0.85} />
      </mesh>
    </group>
  );
}

// Scanner rings that rotate around the cat
interface ScannerRingsProps {
  active: boolean;
}

function ScannerRings({ active }: ScannerRingsProps) {
  const ringRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (!ringRef.current || !active) return;
    ringRef.current.rotation.y = state.clock.getElapsedTime() * 0.3;
    ringRef.current.rotation.x = Math.sin(state.clock.getElapsedTime() * 0.2) * 0.1;
  });

  if (!active) return null;

  return (
    <group ref={ringRef}>
      {[0, 1, 2].map((i) => (
        <mesh key={i} rotation={[Math.PI / 2 + i * 0.3, 0, i * (Math.PI / 3)]}>
          <torusGeometry args={[2.5 + i * 0.3, 0.01, 16, 64]} />
          <meshBasicMaterial
            color="#00ffff"
            transparent
            opacity={0.3 - i * 0.08}
          />
        </mesh>
      ))}
    </group>
  );
}

// Ambient emergence particles
function EmergenceParticles() {
  const particlesRef = useRef<THREE.Points>(null);

  const particles = useMemo(() => {
    const count = 200;
    const positions = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      const radius = 3 + Math.random() * 15;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);

      positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = radius * Math.cos(phi);
    }

    return positions;
  }, []);

  useFrame((state) => {
    if (!particlesRef.current) return;
    particlesRef.current.rotation.y = state.clock.getElapsedTime() * 0.01;
  });

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          args={[particles, 3]}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.015}
        color="#94a3b8"
        transparent
        opacity={0.15}
        sizeAttenuation
      />
    </points>
  );
}

// Camera controller for the scene
function CameraController() {
  const { camera } = useThree();

  useEffect(() => {
    camera.position.set(0, 4, 10);
    camera.lookAt(0, 1.5, 0);
  }, [camera]);

  return null;
}

// Main component props
interface ByrdCatVisualizationProps {
  rsiPhase?: string;
  systemState?: string;
  showScanners?: boolean;
  showParticles?: boolean;
  className?: string;
  compact?: boolean;
}

export function ByrdCatVisualization({
  rsiPhase = 'idle',
  systemState = 'stopped',
  showScanners = true,
  showParticles = true,
  className = '',
  compact = false,
}: ByrdCatVisualizationProps) {
  const isActive = systemState === 'running' || systemState === 'dreaming';

  return (
    <div className={`relative ${className}`}>
      <Canvas
        shadows
        camera={{
          position: compact ? [0, 3, 8] : [0, 4, 10],
          fov: 45,
        }}
        style={{ background: 'transparent' }}
      >
        {/* Lighting - matching archived version */}
        <ambientLight intensity={0.7} />
        <directionalLight
          position={[5, 10, 5]}
          intensity={1.0}
          castShadow
          shadow-mapSize={[2048, 2048]}
        />
        <directionalLight position={[-5, 5, -5]} intensity={0.5} />
        <directionalLight position={[0, 3, -8]} intensity={0.3} />

        <Suspense fallback={null}>
          <ProceduralCat rsiPhase={rsiPhase} systemState={systemState} />
          {showScanners && <ScannerRings active={isActive} />}
          {showParticles && <EmergenceParticles />}
        </Suspense>

        <CameraController />

        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          minDistance={1.5}
          maxDistance={15}
          target={[0, 1.5, 0]}
          autoRotate
          autoRotateSpeed={0.5}
          enablePan={false}
        />
      </Canvas>

      {/* Vignette overlay for depth */}
      <div className="absolute inset-0 pointer-events-none obs-vignette" />
    </div>
  );
}

export default ByrdCatVisualization;
