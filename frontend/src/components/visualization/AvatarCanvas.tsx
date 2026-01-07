import { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import { Rotate3D } from 'lucide-react';
import { cn } from '@lib/utils/cn';

interface AvatarCanvasProps {
  modelPath?: string;
  animationState?: 'idle' | 'thinking' | 'speaking';
  className?: string;
  autoRotate?: boolean;
}

export function AvatarCanvas({
  animationState = 'idle',
  className,
}: AvatarCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const avatarRef = useRef<THREE.Object3D | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showControls] = useState(true);

  // Initialize Three.js scene
  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf8fafc);
    sceneRef.current = scene;

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

    // Animation loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      // Simple animation based on state
      if (avatarRef.current) {
        const time = Date.now() * 0.001;

        if (animationState === 'idle') {
          avatarRef.current.rotation.y = Math.sin(time * 0.5) * 0.1;
          avatarRef.current.position.y = Math.sin(time * 2) * 0.05;
        } else if (animationState === 'thinking') {
          avatarRef.current.rotation.y = time * 2;
          avatarRef.current.position.y = Math.sin(time * 5) * 0.1;
        } else if (animationState === 'speaking') {
          avatarRef.current.rotation.y = Math.sin(time * 3) * 0.2;
          avatarRef.current.scale.y = 1 + Math.sin(time * 10) * 0.05;
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
      const width = container.clientWidth;
      const height = container.clientHeight;
      cameraRef.current.aspect = width / height;
      cameraRef.current.updateProjectionMatrix();
      rendererRef.current.setSize(width, height);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      if (rendererRef.current && container.contains(rendererRef.current.domElement)) {
        container.removeChild(rendererRef.current.domElement);
      }
      rendererRef.current?.dispose();
    };
  }, [animationState]);

  function createProceduralAvatar(scene: THREE.Scene) {
    // Create a simple box as placeholder avatar
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshStandardMaterial({
      color: 0x7c3aed,
      metalness: 0.3,
      roughness: 0.4,
    });
    const avatar = new THREE.Mesh(geometry, material);
    avatar.position.set(0, 0, 0);
    scene.add(avatar);
    avatarRef.current = avatar;

    // Add eyes
    const eyeGeometry = new THREE.SphereGeometry(0.1, 16, 16);
    const eyeMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0x7c3aed, emissiveIntensity: 0.5 });

    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(-0.2, 0.1, 0.5);
    avatar.add(leftEye);

    const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.position.set(0.2, 0.1, 0.5);
    avatar.add(rightEye);
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

      {/* Camera controls overlay */}
      {showControls && !isLoading && (
        <div className="absolute top-4 right-4 flex gap-2 z-10">
          <button
            onClick={() => {
              if (cameraRef.current) {
                cameraRef.current.position.set(0, 0, 5);
                cameraRef.current.lookAt(0, 0, 0);
              }
            }}
            className="p-2 bg-white dark:bg-slate-700 rounded-lg shadow-lg hover:shadow-xl transition-shadow"
            title="Reset view"
          >
            <Rotate3D className="w-5 h-5 text-slate-700 dark:text-slate-200" />
          </button>
        </div>
      )}
    </div>
  );
}
