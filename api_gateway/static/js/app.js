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
    const publicOperation = operation === 'compra' ? 'comprar' : operation;
    $('#routeLabel').textContent = `POST /api/v1/loja/${publicOperation}/`;
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

function showInventory(items) {
    const body = $('#inventoryBody');
    body.replaceChildren();

    if (!items.length) {
        body.innerHTML = '<tr><td colspan="3" class="empty-table">Sua mochila está vazia.</td></tr>';
        return;
    }

    items.forEach((item) => {
        const row = document.createElement('tr');
        [item.nome_item, `#${item.item_id_loja}`, item.quantidade].forEach((value) => {
            const cell = document.createElement('td');
            cell.textContent = value;
            row.appendChild(cell);
        });
        body.appendChild(row);
    });
}

async function loadInventory() {
    if (!state.token) {
        showInventory([]);
        $('#inventoryHint').textContent = 'Gere um token antes de consultar a mochila.';
        $('#inventoryHint').className = 'inventory-hint error-text';
        return;
    }

    const button = $('#inventoryButton');
    button.disabled = true;
    $('#inventoryHint').textContent = 'Consultando inventário...';
    $('#inventoryHint').className = 'inventory-hint';

    try {
        const response = await fetch('/api/v1/mochila/', {
            headers: { Authorization: `Bearer ${state.token}` },
            cache: 'no-store',
        });
        const payload = await response.json();

        if (!response.ok) {
            throw new Error(payload.detail || payload.erro || 'Não foi possível consultar a mochila.');
        }

        showInventory(payload);
        $('#inventoryHint').textContent = `${payload.length} item(ns) encontrado(s).`;
    } catch (error) {
        showInventory([]);
        $('#inventoryHint').textContent = error.message;
        $('#inventoryHint').className = 'inventory-hint error-text';
    } finally {
        button.disabled = false;
    }
}

document.querySelectorAll('.tab').forEach((tab) => tab.addEventListener('click', () => updateOperation(tab.dataset.operation)));
$('#clearToken').addEventListener('click', () => setToken(''));
$('#inventoryButton').addEventListener('click', loadInventory);

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
        const publicOperation = state.operation === 'compra' ? 'comprar' : state.operation;
        const response = await fetch(`/api/v1/loja/${publicOperation}/`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${state.token}` }, body: JSON.stringify({ item_id: Number($('#itemId').value), quantidade: Number($('#quantity').value) }) });
        const payload = await response.json();
        showResponse(payload, response.status, response.ok);
        if (response.ok) loadInventory();
    } catch (error) {
        showResponse({ erro: 'Gateway indisponível ou sem resposta.' }, 0, false);
    }
});

if (state.token) setToken(state.token);
