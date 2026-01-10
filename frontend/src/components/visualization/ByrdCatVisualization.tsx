/**
 * BYRD Cat Consciousness Visualization
 * React Three Fiber port of the archived byrd-cat-visualization.html
 *
 * Displays BYRD's "ego" as a 3D black cat with gold eyes.
 * Eye color and glow intensity respond to RSI phase state.
 */

import { Suspense, useRef, useMemo, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';
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
  if (rsiPhase === 'collapse') return 1.2; // Maximum during quantum collapse
  if (systemState === 'running') return 0.8;
  return 0.6;
};

interface CatModelProps {
  rsiPhase: string;
  systemState: string;
}

// Procedural fallback cat when GLTF model fails to load
function ProceduralCat({ rsiPhase, systemState }: CatModelProps) {
  const catRef = useRef<THREE.Group>(null);
  const leftEyeRef = useRef<THREE.Mesh>(null);
  const rightEyeRef = useRef<THREE.Mesh>(null);

  const eyeColor = RSI_PHASE_COLORS[rsiPhase] || RSI_PHASE_COLORS.idle;

  // Animation loop
  useFrame((state) => {
    if (!catRef.current) return;

    const elapsed = state.clock.getElapsedTime();

    // Breathing animation
    const breathSpeed = systemState === 'dreaming' ? 0.3 : 0.5;
    const breathAmount = systemState === 'dreaming' ? 0.02 : 0.015;
    const breathPhase = Math.sin(elapsed * breathSpeed * Math.PI * 2);

    catRef.current.position.y = breathPhase * breathAmount;

    // Subtle idle sway
    const idlePhase = elapsed * 0.3;
    catRef.current.rotation.y = Math.sin(idlePhase) * 0.02;

    // Eye glow pulse
    const targetIntensity = getEyeIntensity(systemState, rsiPhase);
    const glowPulse = targetIntensity + Math.sin(elapsed * 0.5) * 0.2;

    [leftEyeRef.current, rightEyeRef.current].forEach((eye) => {
      if (eye && eye.material) {
        const mat = eye.material as THREE.MeshStandardMaterial;
        mat.emissiveIntensity = glowPulse;
      }
    });
  });

  return (
    <group ref={catRef} position={[0, 0, 0]}>
      {/* Body - chonky cat shape */}
      <mesh position={[0, 0.5, 0]} castShadow receiveShadow>
        <capsuleGeometry args={[0.8, 1.5, 8, 16]} />
        <meshStandardMaterial color="#0a0a0a" roughness={0.85} metalness={0.05} />
      </mesh>

      {/* Head */}
      <mesh position={[0, 1.4, 0.2]} castShadow receiveShadow>
        <sphereGeometry args={[0.5, 16, 16]} />
        <meshStandardMaterial color="#0a0a0a" roughness={0.85} metalness={0.05} />
      </mesh>

      {/* Left eye */}
      <mesh ref={leftEyeRef} position={[-0.2, 1.45, 0.55]} castShadow>
        <sphereGeometry args={[0.08, 8, 8]} />
        <meshStandardMaterial
          color={eyeColor}
          emissive={eyeColor}
          emissiveIntensity={0.8}
          roughness={0.2}
          metalness={0.3}
        />
      </mesh>

      {/* Right eye */}
      <mesh ref={rightEyeRef} position={[0.2, 1.45, 0.55]} castShadow>
        <sphereGeometry args={[0.08, 8, 8]} />
        <meshStandardMaterial
          color={eyeColor}
          emissive={eyeColor}
          emissiveIntensity={0.8}
          roughness={0.2}
          metalness={0.3}
        />
      </mesh>

      {/* Ears */}
      <mesh position={[-0.3, 1.8, 0.1]} rotation={[0, 0, -0.3]} castShadow>
        <coneGeometry args={[0.2, 0.3, 3]} />
        <meshStandardMaterial color="#0a0a0a" roughness={0.85} />
      </mesh>
      <mesh position={[0.3, 1.8, 0.1]} rotation={[0, 0, 0.3]} castShadow>
        <coneGeometry args={[0.2, 0.3, 3]} />
        <meshStandardMaterial color="#0a0a0a" roughness={0.85} />
      </mesh>

      {/* Tail */}
      <mesh position={[0, 0.3, -0.8]} rotation={[0.3, 0, 0]} castShadow>
        <capsuleGeometry args={[0.1, 1, 4, 8]} />
        <meshStandardMaterial color="#0a0a0a" roughness={0.85} />
      </mesh>
    </group>
  );
}

function CatModel({ rsiPhase, systemState }: CatModelProps) {
  const catRef = useRef<THREE.Group>(null);
  const eyeMeshesRef = useRef<THREE.Mesh[]>([]);

  // Try to load the cat model with error handling
  let scene: THREE.Group | null = null;
  let hasError = false;

  try {
    const result = useGLTF('/models/cat.glb');
    scene = result.scene;
  } catch (e) {
    // Model failed to load - will use procedural fallback
    hasError = true;
  }

  // Fall back to procedural cat if model failed to load
  if (hasError || !scene) {
    return <ProceduralCat rsiPhase={rsiPhase} systemState={systemState} />;
  }

  // Clone the scene to avoid mutation issues
  const catScene = useMemo(() => {
    try {
      const cloned = scene.clone(true);

      // Create materials
      const blackMaterial = new THREE.MeshStandardMaterial({
        color: 0x0a0a0a,
        roughness: 0.85,
        metalness: 0.05,
      });

      const eyeColor = RSI_PHASE_COLORS[rsiPhase] || RSI_PHASE_COLORS.idle;
      const eyeMaterial = new THREE.MeshStandardMaterial({
        color: eyeColor,
        emissive: eyeColor,
        emissiveIntensity: 0.8,
        roughness: 0.2,
        metalness: 0.3,
      });

      // Reset eye meshes array
      eyeMeshesRef.current = [];

      // Apply materials
      cloned.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh;
          mesh.castShadow = true;
          mesh.receiveShadow = true;

          const name = mesh.name.toLowerCase();
          if (name.includes('eye') && !name.includes('lid')) {
            mesh.material = eyeMaterial.clone();
            eyeMeshesRef.current.push(mesh);
          } else {
            mesh.material = blackMaterial.clone();
          }
        }
      });

      // Scale for "chonky" proportions
      cloned.scale.set(3, 2.4, 2.8);

      return cloned;
    } catch (e) {
      // If processing fails, fall back to procedural
      console.warn('Error processing GLTF scene, using procedural fallback:', e);
      return null;
    }
  }, [scene, rsiPhase]);

  // If useMemo failed, use procedural
  if (!catScene) {
    return <ProceduralCat rsiPhase={rsiPhase} systemState={systemState} />;
  }

  // Update eye color when RSI phase changes
  useEffect(() => {
    const eyeColor = RSI_PHASE_COLORS[rsiPhase] || RSI_PHASE_COLORS.idle;
    eyeMeshesRef.current.forEach((mesh) => {
      const material = mesh.material as THREE.MeshStandardMaterial;
      if (material) {
        material.color.set(eyeColor);
        material.emissive.set(eyeColor);
      }
    });
  }, [rsiPhase]);

  // Animation loop
  useFrame((state) => {
    if (!catRef.current) return;

    const elapsed = state.clock.getElapsedTime();

    // Breathing animation - subtle scale on Y axis
    const breathSpeed = systemState === 'dreaming' ? 0.3 : 0.5;
    const breathAmount = systemState === 'dreaming' ? 0.02 : 0.015;
    const breathPhase = Math.sin(elapsed * breathSpeed * Math.PI * 2);

    catRef.current.scale.y = 2.4 + breathPhase * breathAmount;
    catRef.current.scale.x = 3 + breathPhase * breathAmount * 0.3;

    // Subtle idle sway
    const idlePhase = elapsed * 0.3;
    catRef.current.rotation.y = Math.sin(idlePhase) * 0.02;
    catRef.current.rotation.z = Math.sin(idlePhase * 0.7) * 0.008;

    // Eye glow animation
    const targetIntensity = getEyeIntensity(systemState, rsiPhase);
    const glowPulse = targetIntensity + Math.sin(elapsed * 0.5) * 0.2;

    eyeMeshesRef.current.forEach((mesh) => {
      const material = mesh.material as THREE.MeshStandardMaterial;
      if (material && material.emissiveIntensity !== undefined) {
        // Smooth interpolation towards target
        material.emissiveIntensity += (glowPulse - material.emissiveIntensity) * 0.02;
      }
    });
  });

  return (
    <group ref={catRef} position={[0, 0, 0]}>
      <primitive object={catScene} />
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
    const count = 150;
    const positions = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      const radius = 3 + Math.random() * 10;
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
        size={0.02}
        color="#00ffff"
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
    camera.position.set(0, 2, 6);
    camera.lookAt(0, 0.5, 0);
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
          position: compact ? [0, 1.5, 4] : [0, 2, 6],
          fov: compact ? 50 : 45,
        }}
        style={{ background: 'transparent' }}
      >
        {/* Lighting */}
        <ambientLight intensity={0.4} />
        <directionalLight
          position={[5, 10, 5]}
          intensity={0.8}
          castShadow
          shadow-mapSize={[1024, 1024]}
        />
        <directionalLight position={[-5, 5, -5]} intensity={0.3} />

        {/* Point light for cat eye glow effect */}
        <pointLight
          position={[0, 1, 1]}
          intensity={isActive ? 0.5 : 0.2}
          color={RSI_PHASE_COLORS[rsiPhase] || '#64748b'}
          distance={5}
        />

        <Suspense fallback={null}>
          <CatModel rsiPhase={rsiPhase} systemState={systemState} />
          {showScanners && <ScannerRings active={isActive} />}
          {showParticles && <EmergenceParticles />}
        </Suspense>

        <CameraController />

        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          minDistance={compact ? 2 : 3}
          maxDistance={compact ? 8 : 15}
          target={[0, 0.5, 0]}
          autoRotate
          autoRotateSpeed={0.3}
          enablePan={false}
        />
      </Canvas>

      {/* Vignette overlay for depth */}
      <div className="absolute inset-0 pointer-events-none obs-vignette" />
    </div>
  );
}

export default ByrdCatVisualization;
