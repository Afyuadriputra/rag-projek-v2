import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

export default function ChatComposer({
  onSend,
  onUploadClick,
  loading,
}: {
  onSend: (message: string) => void;
  onUploadClick: () => void;
  loading?: boolean;
}) {
  const [value, setValue] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const taRef = useRef<HTMLTextAreaElement | null>(null);

  // Auto-resize logic
  useEffect(() => {
    const ta = taRef.current;
    if (!ta) return;
    ta.style.height = "0px";
    ta.style.height = Math.min(160, ta.scrollHeight) + "px";
  }, [value]);

  const submit = () => {
    const msg = value.trim();
    if (!msg || loading) return;
    onSend(msg);
    setValue("");
    if (taRef.current) taRef.current.style.height = "auto";
  };

  const canSend = !!value.trim() && !loading;

  return (
    // Ubah z-index jadi tinggi (z-50) agar selalu di atas chat
    <div className="absolute bottom-0 left-0 w-full z-50">
      
      {/* Gradient Mask (Pudar ke atas) */}
      <div className="absolute inset-x-0 bottom-0 h-48 bg-gradient-to-t from-white via-white/95 to-transparent pointer-events-none" />

      <div className="relative mx-auto w-full max-w-3xl px-4 pb-4 md:pb-6 pt-2">
        {/* Container Input Utama */}
        <div
          className={cn(
            "relative flex items-end gap-2 p-2 transition-all duration-300",
            // Border & Shape
            "rounded-[26px] border border-black/5 md:rounded-[32px]",
            // Background: Lebih solid di mobile (white/80) agar tidak tembus teks belakang
            "bg-white/80 md:bg-white/60 backdrop-blur-xl backdrop-saturate-150",
            // Shadow
            "shadow-[0_8px_30px_rgba(0,0,0,0.08)]",
            isFocused && "shadow-[0_12px_40px_rgba(0,0,0,0.12)] bg-white/90"
          )}
        >
          {/* Tombol Upload (+ / Attachment) */}
          <button
            type="button"
            onClick={onUploadClick}
            disabled={loading}
            className="flex size-10 flex-shrink-0 items-center justify-center rounded-full text-zinc-400 hover:bg-zinc-100 hover:text-zinc-800 transition-colors"
          >
            <span className="material-symbols-outlined text-[24px]">add_circle</span>
          </button>

          {/* Textarea Input */}
          <div className="flex-1 py-2.5">
            <textarea
              ref={taRef}
              value={value}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              onChange={(e) => setValue(e.target.value)}
              placeholder="Tanya sesuatu..."
              rows={1}
              disabled={loading}
              className={cn(
                "block w-full resize-none bg-transparent px-1",
                "text-[15px] md:text-[16px] leading-relaxed text-zinc-800 placeholder:text-zinc-400",
                "border-none focus:ring-0 focus:outline-none",
                "max-h-[120px] overflow-y-auto scrollbar-hide"
              )}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  submit();
                }
              }}
            />
          </div>

          {/* Tombol Kirim (Panah) */}
          <button
             type="button"
             onClick={submit}
             disabled={!canSend}
             className={cn(
               "flex size-10 flex-shrink-0 items-center justify-center rounded-full transition-all duration-300",
               canSend 
                 ? "bg-black text-white shadow-md scale-100" 
                 : "bg-transparent text-zinc-300 scale-90"
             )}
          >
             <span className="material-symbols-outlined text-[20px]">
               {loading ? "stop" : "arrow_upward"}
             </span>
          </button>
        </div>

        {/* Footer Text (Sembunyikan di Mobile agar tidak numpuk) */}
        <div className="mt-2 text-center hidden md:block">
          <p className="text-[10px] uppercase tracking-[0.2em] text-zinc-400 font-medium">
             Academic AI • Context Aware
          </p>
        </div>
      </div>
    </div>
  );
}