<script>
    import { subscriptions } from "$lib/stores/subscriptions";
    import { goto } from "$app/navigation"; // SvelteKit 페이지 이동 함수
  
    const efficiency = (daysUsed) => {
      if (daysUsed >= 20) return "높음";
      if (daysUsed >= 10) return "중간";
      return "낮음";
    };
  
    let sortDescending = true;
  
    // 정렬 순서 변경 함수
    const toggleSortOrder = () => {
      sortDescending = !sortDescending;
    };
  
    // 지난 통계 데이터 (예시 데이터)
    const pastStatistics = [
      { month: "2024.10월", total: 54099, change: 20 },
      { month: "2024.9월", total: 40000, change: -20 },
      { month: "2024.8월", total: 54000, change: -13 },
    ];
  
    // 세부 통계 페이지로 이동
    const goToDetails = (month) => {
      goto(`/details/${month}`);
    };
  </script>
  
  <main class="statistics">
    <!-- 제목과 정렬 아이콘 -->
    <div class="statistics-header">
      <h1>구독 효율 분석</h1>
      <button class="sort-button" on:click={toggleSortOrder}>
        {#if sortDescending}
          <!-- 내림차순 아이콘 -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
            <path d="M12 16l-6-6h12l-6 6z" />
          </svg>
        {:else}
          <!-- 오름차순 아이콘 -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
            <path d="M12 8l6 6H6l6-6z" />
          </svg>
        {/if}
      </button>
    </div>
  
    <!-- 구독 효율 분석 -->
    {#each $subscriptions as sub}
    <div class="stat-item">
      <!-- 로고와 이름 -->
      <div class="stat-logo-name">
        <img src="{sub.logoUrl}" alt="{sub.name} 로고" class="logo" />
        <h2 class="stat-name">{sub.name}</h2>
      </div>
  
      <!-- 상세 정보 -->
      <div class="stat-details">
        <p>이번 달 사용: {Math.floor(Math.random() * 30)}일</p>
        <p>{sub.price.toLocaleString()}원 / 월</p>
        <p>효율성 지수: {efficiency(Math.floor(Math.random() * 30))}</p>
      </div>
    </div>
    {/each}
  
    <!-- 지난 통계 -->
    <section class="past-statistics">
      <h2 class="past-statistics-title">지난 통계</h2>
      {#each pastStatistics as stat}
      <div
        class="past-stat-item"
        on:click={() => goToDetails(stat.month)}
        role="button"
        tabindex="0"
        aria-label={`통계 ${stat.month}`}
      >
        <div class="month-container">
          <h3 class="month">{stat.month}</h3>
          <div class="stat-change-container">
            <p class="total">총 구독료 {stat.total.toLocaleString()}원</p>
            <p class="change" style="color: {stat.change > 0 ? 'red' : 'blue'};">
              {stat.change > 0 ? `+${stat.change}%` : `${stat.change}%`}
            </p>
          </div>
        </div>
      </div>
      {/each}
    </section>
  </main>
  
  <style>
    .statistics {
      padding: 1rem;
    }
  
    .statistics-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
  
    .sort-button {
      background: none;
      border: none;
      cursor: pointer;
      padding: 0;
      display: flex;
      align-items: center;
    }
  
    .sort-button svg {
      width: 24px;
      height: 24px;
      fill: white;
      transition: transform 0.2s ease;
    }
  
    .sort-button svg:hover {
      transform: scale(1.1);
    }
  
    .stat-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2rem;
      background-color: #000;
      color: white;
      border-radius: 8px;
    }
  
    .stat-logo-name {
      display: flex;
      align-items: center;
      gap: 1rem;
    }
  
    .logo {
      width: 52px;
      height: 52px;
      object-fit: cover;
      border-radius: 8px;
    }
  
    .stat-name {
      font-size: 24px;
      font-weight: bold;
      margin: 0;
    }
  
    .stat-details {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      text-align: right;
    }
  
    .stat-details p {
      margin: 0;
      font-size: 14px;
    }
  
    .past-statistics {
      margin-top: 2rem;
    }
  
    .past-statistics-title {
      font-size: 30px;
      font-weight: bold;
      margin-bottom: 1rem;
    }
  
    .past-stat-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background-color: #000;
      padding: 1rem;
      border-radius: 8px;
      color: white;
      margin-bottom: 1rem;
      cursor: pointer; /* 클릭 가능 */
      transition: background-color 0.2s ease;
    }
  
    .past-stat-item:hover {
      background-color: #222; /* 호버 시 배경색 변경 */
    }
  
    .month-container {
      display: flex; /* 가로 정렬 */
      align-items: center; /* 세로 정렬 */
      justify-content: space-between; /* 요소 간 여백 조정 */
      gap: 1rem; /* 간격 추가 */
      width: 100%; /* 컨테이너 전체 사용 */
    }
  
    .month {
      font-size: 24px;
      font-weight: 900;
      margin: 0;
    }
  
    .stat-change-container {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      text-align: right;
    }
  
    .total {
      font-size: 14px;
      margin: 0;
    }
  
    .change {
      font-size: 14px;
      font-weight: bold;
      margin: 0;
      margin-top: 0.5rem;
    }
  </style>