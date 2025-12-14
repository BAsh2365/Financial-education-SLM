const chatEl = document.getElementById('chat');
const form = document.getElementById('input-form');
const input = document.getElementById('message');

function addMessage(role, text) {
  const el = document.createElement('div');
  el.className = 'message ' + role;
  el.innerText = text;
  chatEl.appendChild(el);
  chatEl.scrollTop = chatEl.scrollHeight;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  addMessage('user', message);
  input.value = '';
  addMessage('bot', 'Thinking...');

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    // Remove the temporary 'Thinking...' message
    const tmp = chatEl.querySelector('.message.bot:last-child');
    if (tmp && tmp.innerText === 'Thinking...') tmp.remove();

    if (data.stock_price_info) {
      addMessage('bot', data.stock_price_info);
    }
    if (data.reply) {
      addMessage('bot', data.reply);
    } else if (data.error) {
      addMessage('bot', 'Error: ' + data.error);
    }
  } catch (err) {
    const tmp = chatEl.querySelector('.message.bot:last-child');
    if (tmp && tmp.innerText === 'Thinking...') tmp.remove();
    addMessage('bot', 'Network error');
  }
});
