'use client';

import { useState, useEffect } from 'react';
import { useTutorStore } from '@/lib/store';
import { SessionStart } from '@/components/SessionStart';
import { ChatInterface } from '@/components/ChatInterface';

export default function Home() {
  const sessionId = useTutorStore((state) => state.sessionId);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return <>{sessionId ? <ChatInterface /> : <SessionStart />}</>;
}
