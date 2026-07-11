/**
 * LogInteraction page — the main page composing the split-screen layout.
 *
 * Layout: 60% left panel (form) | 40% right panel (chat)
 * Matches the assignment screenshot.
 */

import InteractionForm from '../components/form/InteractionForm';
import ChatPanel from '../components/chat/ChatPanel';

export default function LogInteraction() {
  return (
    <div className="h-screen bg-[#f8fafc] flex flex-col p-6 font-sans overflow-hidden">
      <h1 className="text-2xl font-bold text-[#1e293b] mb-6 font-serif">Log HCP Interaction</h1>
      
      <div className="flex flex-1 gap-6 max-w-[1400px] mx-auto w-full overflow-hidden">
        {/* Left Panel — Interaction Form (60%) */}
        <div className="w-[65%] bg-white rounded shadow-sm border border-gray-200 flex flex-col overflow-hidden">
          <InteractionForm />
        </div>

        {/* Right Panel — AI Chat (35%) */}
        <div className="w-[35%] bg-white rounded shadow-sm border border-gray-200 flex flex-col overflow-hidden">
          <ChatPanel />
        </div>
      </div>
    </div>
  );
}
