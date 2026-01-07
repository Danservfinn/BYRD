import { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
// @ts-ignore - OrbitControls is in examples/jsm which TypeScript doesn't always resolve correctly
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { Rotate3D, Info, Camera, Home } from 'lucide-react';
import { cn } from '@lib/utils/cn';

interface AvatarCanvasProps {
  modelPath?: string;
  animationState?: 'idle' | 'thinking' | 'speaking';
  className?: string;
  autoRotate?: boolean;
}

interface CameraPreset {
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  position: [number, number, number];
  target: [number, number, number];
}

const CAMERA_PRESETS: CameraPreset[] = [
  { name: 'Front', icon: Home, position: [0, 0, 5] as [number, number, number], target: [0, 0, 0] as [number, number, number] },
  { name: 'Top', icon: Camera, position: [0, 5, 0] as [number, number, number], target: [0, 0, 0] as [number, number, number] },
  { name: 'Side', icon: Camera, position: [5, 0, 0] as [number, number, number], target: [0, 0, 0] as [number, number, number] },
];

export function AvatarCanvas({
  animationState = 'idle',
  className,
}: AvatarCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const avatarRef = useRef<THREE.Object3D | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showInfo, setShowInfo] = useState(false);
  const [showPresets, setShowPresets] = useState(false);

  const moveToPreset = (preset: CameraPreset) => {
    if (cameraRef.current && controlsRef.current) {
      const { position, target } = preset;
      cameraRef.current.position.set(...position);
      controlsRef.current.target.set(...target);
    }
  };

  // Initialize Three.js scene
  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const getDimensions = () => ({
      width: container.clientWidth || 1,
      height: container.clientHeight || 1,
    });

    let { width, height } = getDimensions();

    // Scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf1f5f9); // Slightly darker for visibility
    sceneRef.current = scene;

    console.log('[AvatarCanvas] Scene initialized', { width, height });

    // Camera
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 0, 5);
    cameraRef.current = camera;

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.enableZoom = true;
    controls.minDistance = 2;
    controls.maxDistance = 10;
    controls.enablePan = false;
    controlsRef.current = controls;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 1);
    keyLight.position.set(5, 5, 5);
    keyLight.castShadow = true;
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0xffffff, 0.5);
    fillLight.position.set(-5, 3, 2);
    scene.add(fillLight);

    const rimLight = new THREE.DirectionalLight(0x7c3aed, 0.8);
    rimLight.position.set(0, 5, -5);
    scene.add(rimLight);

    // Create procedural avatar (box for now, will be replaced with loaded model)
    createProceduralAvatar(scene);

    setIsLoading(false);
    console.log('[AvatarCanvas] Scene initialization complete');

    // Animation loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      // Update controls for damping
      controls.update();

      // Animate avatar based on state
      if (avatarRef.current && avatarRef.current.children) {
        const time = Date.now() * 0.001;

        // Core sphere (index 0)
        const core = avatarRef.current.children[0] as THREE.Mesh;
        // Wireframe shell (index 1)
        const shell = avatarRef.current.children[1] as THREE.Mesh;
        // Rings (indices 2, 3, 4)
        const ring1 = avatarRef.current.children[2] as THREE.Mesh;
        const ring2 = avatarRef.current.children[3] as THREE.Mesh;
        const ring3 = avatarRef.current.children[4] as THREE.Mesh;

        if (animationState === 'idle') {
          // Gentle floating and slow rotation
          avatarRef.current.position.y = Math.sin(time * 1.5) * 0.08;
          avatarRef.current.rotation.y = Math.sin(time * 0.3) * 0.15;

          // Slow ring rotations
          if (ring1) ring1.rotation.z = time * 0.2;
          if (ring2) ring2.rotation.x = Math.PI / 3 + Math.sin(time * 0.15) * 0.2;
          if (ring3) ring3.rotation.y = time * 0.25;

          // Subtle shell pulsing
          if (shell && shell.scale) {
            const scale = 1 + Math.sin(time * 2) * 0.05;
            shell.scale.set(scale, scale, scale);
          }
        } else if (animationState === 'thinking') {
          // Fast rotation, elevated position
          avatarRef.current.rotation.y = time * 1.5;
          avatarRef.current.rotation.x = Math.sin(time * 2) * 0.1;
          avatarRef.current.position.y = Math.sin(time * 3) * 0.12 + 0.2;

          // Rapid ring rotations in different directions
          if (ring1) {
            ring1.rotation.z = time * 0.8;
            ring1.rotation.x = Math.sin(time * 2) * 0.3;
          }
          if (ring2) {
            ring2.rotation.x = time * 0.6;
            ring2.rotation.y = Math.cos(time * 1.5) * 0.4;
          }
          if (ring3) {
            ring3.rotation.y = time * 0.7;
            ring3.rotation.z = Math.sin(time * 2.5) * 0.3;
          }

          // Shell expanding/contracting rapidly
          if (shell && shell.scale) {
            const scale = 1 + Math.sin(time * 8) * 0.15;
            shell.scale.set(scale, scale, scale);
          }

          // Core pulses faster
          if (core && core.scale) {
            const pulse = 1 + Math.sin(time * 10) * 0.1;
            core.scale.set(pulse, pulse, pulse);
          }
        } else if (animationState === 'speaking') {
          // Rhythmic movement simulating speech
          avatarRef.current.rotation.y = Math.sin(time * 5) * 0.2;
          avatarRef.current.position.y = Math.sin(time * 8) * 0.05;

          // Ring waves ripple outward
          if (ring1) ring1.rotation.z = Math.sin(time * 4) * 0.3;
          if (ring2) ring2.rotation.x = Math.sin(time * 4 + 1) * 0.3;
          if (ring3) ring3.rotation.y = Math.sin(time * 4 + 2) * 0.3;

          // Shell breathes rhythmically
          if (shell && shell.scale) {
            const scale = 1 + Math.sin(time * 6) * 0.08;
            shell.scale.set(scale, scale, scale);
          }

          // Core pulses with speech rhythm
          if (core && core.scale) {
            const pulse = 1 + Math.sin(time * 12) * 0.08;
            core.scale.set(pulse, pulse, pulse);
          }
        }
      }

      if (rendererRef.current && sceneRef.current && cameraRef.current) {
        rendererRef.current.render(sceneRef.current, cameraRef.current);
      }
    };
    animate();

    // Handle resize
    const handleResize = () => {
      if (!container || !cameraRef.current || !rendererRef.current) return;
      const width = container.clientWidth || 1;
      const height = container.clientHeight || 1;
      cameraRef.current.aspect = width / height;
      cameraRef.current.updateProjectionMatrix();
      rendererRef.current.setSize(width, height);
    };
    window.addEventListener('resize', handleResize);

    // Also use ResizeObserver for container changes
    const resizeObserver = new ResizeObserver(() => {
      handleResize();
    });
    resizeObserver.observe(container);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      resizeObserver.disconnect();
      cancelAnimationFrame(animationFrameId);
      controls.dispose();
      if (rendererRef.current && container.contains(rendererRef.current.domElement)) {
        container.removeChild(rendererRef.current.domElement);
      }
      rendererRef.current?.dispose();
    };
  }, [animationState]);

  // Auto-hide info after 5 seconds
  useEffect(() => {
    if (showInfo) {
      const timer = setTimeout(() => setShowInfo(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [showInfo]);

  function createProceduralAvatar(scene: THREE.Scene) {
    console.log('[AvatarCanvas] Creating procedural avatar...');
    // Create a sophisticated AI core avatar
    const avatarGroup = new THREE.Group();

    // Core sphere (the "brain")
    const coreGeometry = new THREE.IcosahedronGeometry(0.5, 1);
    const coreMaterial = new THREE.MeshStandardMaterial({
      color: 0x7c3aed,
      metalness: 0.7,
      roughness: 0.2,
      emissive: 0x7c3aed,
      emissiveIntensity: 0.3,
      wireframe: false,
    });
    const core = new THREE.Mesh(coreGeometry, coreMaterial);
    avatarGroup.add(core);

    // Outer wireframe shell
    const shellGeometry = new THREE.IcosahedronGeometry(0.7, 2);
    const shellMaterial = new THREE.MeshBasicMaterial({
      color: 0xa78bfa,
      wireframe: true,
      transparent: true,
      opacity: 0.4,
    });
    const shell = new THREE.Mesh(shellGeometry, shellMaterial);
    avatarGroup.add(shell);

    // Orbital rings (representing recursive thought)
    const ringMaterial = new THREE.MeshStandardMaterial({
      color: 0x7c3aed,
      metalness: 0.8,
      roughness: 0.1,
      emissive: 0x7c3aed,
      emissiveIntensity: 0.2,
    });

    const ring1Geometry = new THREE.TorusGeometry(0.9, 0.02, 16, 100);
    const ring1 = new THREE.Mesh(ring1Geometry, ringMaterial);
    ring1.rotation.x = Math.PI / 2;
    avatarGroup.add(ring1);

    const ring2Geometry = new THREE.TorusGeometry(1.0, 0.02, 16, 100);
    const ring2 = new THREE.Mesh(ring2Geometry, ringMaterial);
    ring2.rotation.x = Math.PI / 3;
    ring2.rotation.y = Math.PI / 6;
    avatarGroup.add(ring2);

    const ring3Geometry = new THREE.TorusGeometry(0.85, 0.02, 16, 100);
    const ring3 = new THREE.Mesh(ring3Geometry, ringMaterial);
    ring3.rotation.y = Math.PI / 4;
    avatarGroup.add(ring3);

    // Glowing "eyes" - energy points that represent consciousness
    const eyeGeometry = new THREE.SphereGeometry(0.12, 32, 32);
    const eyeMaterial = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      emissive: 0x7c3aed,
      emissiveIntensity: 0.8,
      metalness: 0.9,
      roughness: 0.1,
    });

    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(-0.25, 0.15, 0.5);
    avatarGroup.add(leftEye);

    const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.position.set(0.25, 0.15, 0.5);
    avatarGroup.add(rightEye);

    // Add point light at center for glow effect
    const centerLight = new THREE.PointLight(0x7c3aed, 1, 3);
    centerLight.position.set(0, 0, 0);
    avatarGroup.add(centerLight);

    // Position the entire avatar
    avatarGroup.position.set(0, 0, 0);
    scene.add(avatarGroup);
    avatarRef.current = avatarGroup;
    console.log('[AvatarCanvas] Avatar created successfully', { children: avatarGroup.children.length });
  }

  return (
    <div
      ref={containerRef}
      className={cn(
        "relative w-full h-full bg-gradient-to-b from-slate-50 to-white dark:from-slate-900 dark:to-slate-800",
        className
      )}
    >
      {/* Loading state */}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-slate-100 dark:bg-slate-800">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600" />
        </div>
      )}

      {/* Controls overlay */}
      {!isLoading && (
        <div className="absolute top-4 right-4 flex gap-2 z-10">
          <button
            onClick={() => setShowPresets(!showPresets)}
            className="p-2 bg-white dark:bg-slate-700 rounded-lg shadow-lg hover:shadow-xl transition-shadow focus:outline-none focus:ring-2 focus:ring-purple-500"
            title="Camera presets"
            aria-label="Show camera presets"
          >
            <Camera className="w-5 h-5 text-slate-700 dark:text-slate-200" />
          </button>

          <button
            onClick={() => setShowInfo(!showInfo)}
            className="p-2 bg-white dark:bg-slate-700 rounded-lg shadow-lg hover:shadow-xl transition-shadow focus:outline-none focus:ring-2 focus:ring-purple-500"
            title="Show controls info"
            aria-label="Show controls info"
          >
            <Info className="w-5 h-5 text-slate-700 dark:text-slate-200" />
          </button>

          <button
            onClick={() => {
              if (cameraRef.current && controlsRef.current) {
                cameraRef.current.position.set(0, 0, 5);
                controlsRef.current.target.set(0, 0, 0);
              }
            }}
            className="p-2 bg-white dark:bg-slate-700 rounded-lg shadow-lg hover:shadow-xl transition-shadow focus:outline-none focus:ring-2 focus:ring-purple-500"
            title="Reset view"
            aria-label="Reset camera view"
          >
            <Rotate3D className="w-5 h-5 text-slate-700 dark:text-slate-200" />
          </button>
        </div>
      )}

      {/* Info panel */}
      {showInfo && !isLoading && (
        <div className="absolute top-4 left-4 z-10 max-w-xs">
          <div className="bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm rounded-lg shadow-lg p-3 text-xs space-y-2">
            <h3 className="font-semibold text-slate-900 dark:text-slate-100">Controls</h3>
            <div className="space-y-1 text-slate-600 dark:text-slate-400">
              <p>🖱️ <strong>Drag</strong> to rotate</p>
              <p>🤏 <strong>Pinch</strong> to zoom</p>
              <p>✋ <strong>Two-finger</strong> to pan (disabled)</p>
            </div>
            <div className="pt-2 border-t border-slate-200 dark:border-slate-700">
              <p className="text-[10px] text-slate-500 dark:text-slate-500">
                AI Core avatar with recursive orbital rings
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Camera presets panel */}
      {showPresets && !isLoading && (
        <div className="absolute top-16 right-4 z-10 flex flex-col gap-2">
          {CAMERA_PRESETS.map((preset) => {
            const Icon = preset.icon;
            return (
              <button
                key={preset.name}
                onClick={() => moveToPreset(preset)}
                className="p-2 bg-white dark:bg-slate-700 rounded-lg shadow-lg hover:shadow-xl transition-shadow focus:outline-none focus:ring-2 focus:ring-purple-500"
                title={`Move to ${preset.name} view`}
                aria-label={`Switch to ${preset.name} camera view`}
              >
                <Icon className="w-5 h-5 text-slate-700 dark:text-slate-200" />
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
