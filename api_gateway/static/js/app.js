const state = { operation: 'compra', token: localStorage.getItem('goblin_access_token') || '' };
const $ = (selector) => document.querySelector(selector);

function showResponse(payload, status, ok) {
    $('#responseOutput').textContent = JSON.stringify(payload, null, 2);
    $('#responseStatus').textContent = status ? `${status} · ${ok ? 'sucesso' : 'erro'}` : 'falha de conexão';
    $('#responseStatus').className = `response-status ${ok ? 'success' : 'error'}`;
}

function updateOperation(operation) {
    state.operation = operation;
    const isBuy = operation === 'compra';
    document.querySelectorAll('.tab').forEach((tab) => {
        const active = tab.dataset.operation === operation;
        tab.classList.toggle('active', active);
        tab.setAttribute('aria-selected', active);
    });
    $('#routeLabel').textContent = `POST /api/v1/loja/${operation}/`;
    $('#tradeButton').textContent = `Confirmar ${isBuy ? 'compra' : 'venda'} `;
    $('#tradeButton').className = `button primary ${isBuy ? 'buy-action' : 'sell-action'}`;
    $('#tradeButton').insertAdjacentHTML('beforeend', '<span>↗</span>');
}

function setToken(token) {
    state.token = token;
    if (token) {
        localStorage.setItem('goblin_access_token', token);
        $('#tokenState').textContent = 'Token carregado e pronto para uso';
        $('#tokenState').className = 'token-state ok';
    } else {
        localStorage.removeItem('goblin_access_token');
        $('#tokenState').textContent = 'Nenhum token carregado';
        $('#tokenState').className = 'token-state';
    }
}

document.querySelectorAll('.tab').forEach((tab) => tab.addEventListener('click', () => updateOperation(tab.dataset.operation)));
$('#clearToken').addEventListener('click', () => setToken(''));

$('#loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
        const response = await fetch('/api/v1/token/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username: $('#username').value, password: $('#password').value }) });
        const payload = await response.json();
        if (!response.ok || !payload.access) throw new Error(payload.detail || 'Não foi possível autenticar.');
        setToken(payload.access);
        showResponse({ mensagem: 'Token gerado com sucesso.' }, response.status, true);
    } catch (error) {
        showResponse({ erro: error.message }, 0, false);
    }
});

$('#tradeForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!state.token) {
        showResponse({ erro: 'Gere um token antes de realizar a operação.' }, 401, false);
        return;
    }
    try {
        const response = await fetch(`/api/v1/loja/${state.operation}/`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${state.token}` }, body: JSON.stringify({ item_id: Number($('#itemId').value), quantidade: Number($('#quantity').value) }) });
        const payload = await response.json();
        showResponse(payload, response.status, response.ok);
    } catch (error) {
        showResponse({ erro: 'Gateway indisponível ou sem resposta.' }, 0, false);
    }
});

if (state.token) setToken(state.token);
