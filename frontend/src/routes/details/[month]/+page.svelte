<script>
  import { onMount } from "svelte";
  import { subscriptions } from "$lib/stores/subscriptions";

  // 동적 세그먼트에서 전달된 month 값 가져오기
  export let data;
  $: selectedMonth = data.params.month;

  let detailedSubscriptions = [];
  let totalCost = 0;

  // 데이터 초기화
  onMount(() => {
    // 선택된 월에 해당하는 구독 항목 필터링
    detailedSubscriptions = $subscriptions.filter(
      (sub) => sub.renewalMonth === selectedMonth
    );

    // 총 비용 계산
    totalCost = detailedSubscriptions.reduce((sum, sub) => sum + sub.price, 0);
  });
</script>

<main class="detail-page">
  <!-- 헤더 -->
  <header class="header">
    <h1>세부 통계</h1>
    <h2>{selectedMonth}</h2>
  </header>

  <!-- 구독 리스트 -->
  <section class="subscription-list">
    {#if detailedSubscriptions.length > 0}
      {#each detailedSubscriptions as sub}
        <div class="subscription-item">
          <!-- 로고 -->
          <div class="logo">
            <img src="{sub.logoUrl}" alt="{sub.name} 로고" />
          </div>
          <!-- 이름 및 비용 -->
          <div class="details">
            <h3>{sub.name}</h3>
            <p>{sub.price.toLocaleString()}원 / 월</p>
          </div>
        </div>
      {/each}
    {:else}
      <p>해당 월에 갱신된 구독이 없습니다.</p>
    {/if}
  </section>

  <!-- 총 구독료 -->
  <footer class="total-cost">
    <div class="total-text">총 구독료</div>
    <div class="total-value">{totalCost.toLocaleString()} 원</div>
  </footer>
</main>

<style>
  .detail-page {
    background-color: #000;
    color: white;
    padding: 1rem;
    min-height: 100vh;
  }

  .header {
    text-align: left;
    margin-bottom: 2rem;
  }

  .header h1 {
    font-size: 24px;
    margin: 0;
  }

  .header h2 {
    font-size: 18px;
    margin: 0;
    color: #999;
  }

  .subscription-list {
    margin-bottom: 2rem;
  }

  .subscription-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    margin-bottom: 1rem;
    background-color: #222;
    border-radius: 8px;
  }

  .logo img {
    height: 50px;
    width: 50px;
    object-fit: cover;
    border-radius: 8px;
  }

  .details {
    flex-grow: 1;
    margin-left: 1rem;
    text-align: left;
  }

  .details h3 {
    margin: 0;
    font-size: 18px;
    font-weight: bold;
  }

  .details p {
    margin: 0;
    font-size: 14px;
    color: #aaa;
  }

  .total-cost {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #111;
    border-radius: 8px;
  }

  .total-text {
    font-size: 18px;
    font-weight: bold;
  }

  .total-value {
    font-size: 18px;
    font-weight: bold;
    color: #007AFF;
  }
</style>