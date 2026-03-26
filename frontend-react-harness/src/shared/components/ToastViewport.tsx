import { dismissToast, useUiState } from "../lib/uiStore";

export function ToastViewport() {
  const { toasts } = useUiState();

  if (toasts.length === 0) {
    return null;
  }

  return (
    <section aria-live="polite" className="toast-viewport">
      {toasts.map((toast) => (
        <article className={`toast-card toast-${toast.tone}`} key={toast.id}>
          <div>
            <strong>{toast.title}</strong>
            <p>{toast.description}</p>
          </div>
          <button
            aria-label="关闭通知"
            className="toast-close"
            onClick={() => dismissToast(toast.id)}
            type="button"
          >
            关闭
          </button>
        </article>
      ))}
    </section>
  );
}
