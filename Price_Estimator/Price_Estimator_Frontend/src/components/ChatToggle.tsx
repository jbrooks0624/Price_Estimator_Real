"use client";
import { ChatBubbleLeftRightIcon } from "@heroicons/react/24/outline";
import React from "react";

interface ChatToggleProps {
  onClick: () => void;
}

/**
 * Floating circular button used to open the chat sidebar (top-right).
 */
const ChatToggle: React.FC<ChatToggleProps> = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      aria-label="Open chat"
      className="fixed top-6 right-6 z-50 flex h-12 w-12 items-center justify-center rounded-full bg-white border-2 border-black p-2 text-black shadow hover:bg-gray-50"
    >
      <ChatBubbleLeftRightIcon className="h-6 w-6" />
    </button>
  );
};

export default ChatToggle;
