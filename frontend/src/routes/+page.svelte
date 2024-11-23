<script>
    import SubscriptionItem from "$lib/components/SubscriptionItem.svelte";
    import { subscriptions } from "$lib/stores/subscriptions";
    import { goto } from "$app/navigation";
    import { derived } from "svelte/store";
  
    const toggleUsage = (id) => {
      subscriptions.update((subs) => {
        const index = subs.findIndex((sub) => sub.id === id);
        if (index !== -1) {
          subs[index].usedToday = !subs[index].usedToday;
        }
        return subs;
      });
    };
  
    const deleteSubscription = (id) => {
      subscriptions.update((subs) => subs.filter((sub) => sub.id !== id));
    };
  
    const totalCost = derived(subscriptions, ($subscriptions) =>
      $subscriptions.reduce((acc, sub) => acc + sub.price, 0)
    );
  </script>
  <p></p>
  <main class="home">
  <p></p>

    <header class="header">
        <h1 class="header-title">이번 달 나의 구독료</h1>
        <div class="total-cost-container">
          <p class="total-cost">{`${$totalCost.toLocaleString()}원`}</p>
          <p class="total-cost-change">{`지난 달에 비해 ${$totalCost}% 증가했습니다.`}</p>
        </div>
      </header>
    
    

    <section class="subscription-list">
      <h2 class="subscription-list-title">나의 구독목록</h2>
      {#each $subscriptions as subscription}
        <SubscriptionItem
          {subscription}
          class="subscription-item"
          onToggleUsage={toggleUsage}
          onDelete={deleteSubscription}
        />
      {/each}
    </section>
  </main>
  
  <style>
    .home {
        display: flex;
        flex-direction: column;
      background-color: #000000; /* Tailwind bg-gray-900 */
      color: white;
      min-height: 100vh;
      padding: 1rem;
    }
  
    .header {
  display: flex;
  flex-direction: column; /* 세로 정렬 */
  align-items: flex-start; /* 제목을 좌측 정렬 */
}

.header-title {
  text-align: left; /* 제목을 좌측 정렬 */
  font-size: 30px;
  margin: 0; /* 기본 여백 제거 */
  padding-bottom: 10px; /* 내부 여백 제거 */
}

.total-cost-container {
  width: 100%; /* 전체 컨테이너의 너비를 차지 */
  text-align: center; /* 구독료와 설명 텍스트는 중앙 정렬 */
  margin-top: 0.5rem;
}

.total-cost {
  font-size: 24px;
  font-weight: bold;
  color: #007AFF;
  margin: 0;
}

.total-cost-change {
  width: 100%; /* 텍스트를 화면 중앙에 맞추기 위해 */
  text-align: center; /* 중앙 정렬 유지 */
  font-size: 10px;
  color: #FFF;
  margin: 0;
}
    .add-button {
      background-color: #4299e1; /* Tailwind bg-blue-500 */
      color: white;
      padding: 0.5rem 1rem;
      border-radius: 9999px; /* Tailwind rounded-full */
      margin-top: 1rem;
    }
  
    .subscription-list {
      margin-top: 3rem; /* "나의 구독목록"과 리스트 사이의 간격 */
      padding: 1rem 0;
    }
  
    .subscription-list-title {
      font-size: 24px;
      font-weight: 600;
    }
  
    .subscription-item {
      margin-bottom: 1rem;
    }
  </style>