function formatINR(number) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(number);
}

function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast-notice toast-${type}`;
  toast.style.position = 'fixed';
  toast.style.bottom = '24px';
  toast.style.right = '24px';
  toast.style.background = type === 'success' ? '#059669' : '#dc2626';
  toast.style.color = '#fff';
  toast.style.padding = '12px 20px';
  toast.style.borderRadius = '8px';
  toast.style.boxShadow = '0 10px 25px rgba(0,0,0,0.4)';
  toast.style.zIndex = '9999';
  toast.style.fontSize = '0.9rem';
  toast.style.fontWeight = '500';
  toast.textContent = message;

  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, 3500);
}

function openModal(modalId) {
  const el = document.getElementById(modalId);
  if (el) el.style.display = 'flex';
}

function closeModal(modalId) {
  const el = document.getElementById(modalId);
  if (el) el.style.display = 'none';
}

window.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.style.display = 'none';
  }
});

async function reseedDatabaseDemo() {
  if (!confirm("Load sample financial records?")) return;
  try {
    const res = await fetch('/api/seed-database', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showToast("Sample data loaded.");
      setTimeout(() => location.reload(), 1000);
    } else {
      showToast(data.error || "Failed to load sample data.", "error");
    }
  } catch (err) {
    showToast("Error connecting to server.", "error");
  }
}
