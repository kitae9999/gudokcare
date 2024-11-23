<script>
  import { subscriptions } from "$lib/stores/subscriptions";
  let name = "";
  let price = 0;
  let startDate = "";
  let endDate = "";
  let autoRenewal = false;

  const addSubscription = () => {
    subscriptions.update((subs) => [
      ...subs,
      { id: Date.now(), name, price, startDate, endDate, autoRenewal, usedToday: false }
    ]);
    window.location.href = "/";
  };
</script>

<main class="add-subscription">
  <div class="header">
    <h1>구독 추가</h1>
    <button class="complete-button" on:click={addSubscription}>완료</button>
  </div>
  <form on:submit|preventDefault={addSubscription}>
    <div class="input-group">
      <label>서비스명</label>
      <input type="text" bind:value={name} required />
    </div>
    <div class="input-group">
      <label>월간 구독료</label>
      <input type="number" bind:value={price} required />
    </div>
    <div class="input-group">
      <label>구독 시작일</label>
      <input type="date" bind:value={startDate} required />
    </div>
    <div class="input-group">
      <label>구독 만료일</label>
      <input type="date" bind:value={endDate} />
    </div>
    <div class="input-group">
      <label>자동 갱신</label>
      <!-- 토글 스위치 -->
      <label class="toggle-switch">
        <input type="checkbox" bind:checked={autoRenewal} />
        <span class="slider"></span>
      </label>
    </div>
  </form>
</main>

<style>
  .add-subscription {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    color: white;
    background-color: #000;
    height: 100vh;
    box-sizing: border-box;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 2rem;
  }

  .header h1 {
    font-size: 24px;
    margin: 0;
  }

  .complete-button {
    background-color: #007AFF;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 12px;
    cursor: pointer;
    font-size: 16px;
  }

  .complete-button:hover {
    background-color: #005BBB;
  }

  form {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 400px;
  }

  .input-group {
    margin-bottom: 1rem;
    background-color: #222;
    border-radius: 12px;
    padding: 1rem;
  }

  .input-group label {
    display: block;
    font-size: 16px;
    margin-bottom: 0.5rem;
  }

  .input-group input {
    width: 100%;
    font-size: 16px;
    padding: 0.5rem;
    border: none;
    border-radius: 8px;
    background-color: #333;
    color: white;
    box-sizing: border-box;
  }

  /* 토글 스위치 스타일 */
  .toggle-switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 25px;
  }

  .toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: 0.4s;
    border-radius: 34px;
  }

  .slider:before {
    position: absolute;
    content: "";
    height: 19px;
    width: 19px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: 0.4s;
    border-radius: 50%;
  }

  input:checked + .slider {
    background-color: #007AFF;
  }

  input:checked + .slider:before {
    transform: translateX(24px);
  }

  .input-group input:focus {
    outline: none;
    border: 2px solid #007AFF;
  }
</style>