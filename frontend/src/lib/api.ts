import axios from "axios";

// ==========================================
// 1. SETUP AXIOS INSTANCE
// ==========================================
const apiClient = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
  // Konfigurasi untuk Django CSRF Protection
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
  withCredentials: true,
});

// ==========================================
// 2. TIPE DATA (INTERFACES)
// ==========================================

// ✅ Chat API
export interface ChatResponse {
  answer?: string; // backend sukses -> {answer}
  error?: string;  // backend error -> {error}
}

// ✅ Upload API
export interface UploadResponse {
  status: "success" | "error";
  msg: string;
}

// ✅ Documents API (BARU)
export interface DocumentDto {
  id: number;
  title: string;
  is_embedded: boolean;
  uploaded_at: string; // "YYYY-MM-DD HH:MM"
  size_bytes: number;
}

// ✅ Documents API response (BARU)
export interface DocumentsResponse {
  documents: DocumentDto[];
  storage: {
    used_bytes: number;
    quota_bytes: number;
    used_pct: number;
    used_human?: string;  // dari backend (optional)
    quota_human?: string; // dari backend (optional)
  };
}

// ==========================================
// 3. API FUNCTIONS (FUNGSI UTAMA DITANDAI)
// ==========================================

/** ⭐ FUNGSI UTAMA #1: CHAT
 * Mengirim pesan chat ke AI
 * URL Backend: POST /api/chat/
 */
export const sendChat = async (message: string) => {
  // Payload harus match dengan `json.loads(request.body)` di views.py
  const response = await apiClient.post<ChatResponse>("/chat/", { message });
  return response.data;
};

/** ⭐ FUNGSI UTAMA #2: UPLOAD DOCUMENTS
 * Upload banyak file sekaligus
 * URL Backend: POST /api/upload/
 */
export const uploadDocuments = async (files: FileList) => {
  const formData = new FormData();

  // Masukkan semua file ke FormData dengan key 'files'
  // (Sesuai `request.FILES.getlist('files')` di views.py)
  Array.from(files).forEach((file) => {
    formData.append("files", file);
  });

  const response = await apiClient.post<UploadResponse>("/upload/", formData, {
    headers: {
      // Wajib ubah Content-Type agar server tahu ini file upload
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

/** ⭐ FUNGSI UTAMA #3: GET DOCUMENTS (BARU)
 * Ambil daftar dokumen + storage untuk sidebar (refresh setelah upload)
 * URL Backend: GET /api/documents/
 */
export const getDocuments = async () => {
  const response = await apiClient.get<DocumentsResponse>("/documents/");
  return response.data;
};

export default apiClient;
