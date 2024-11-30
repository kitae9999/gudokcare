<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let usageAnalysis = [];
  let usagePatterns = [];

  const API_BASE_URL = 'http://127.0.0.1:8000/contracts';
  const API_TOKEN = localStorage.getItem('token');

   // 사용 효율성 분석 데이터 가져오기
   const fetchUsageAnalysis = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/user/usage-analysis`, {
      headers: {
        Authorization: `Bearer ${API_TOKEN}`,
      },
    });

    if (response.ok) {
      const rawData = await response.json();

      // 각 분석 객체에 logoUrl 추가
      usageAnalysis = rawData.map((analysis) => ({
        ...analysis,
        logoUrl: getLogoUrl(analysis.service_name),
      }));
    } else {
      console.error('사용 효율성 분석 데이터를 가져오는데 실패했습니다.');
    }
  } catch (error) {
    console.error('사용 효율성 분석 데이터 가져오기 중 오류 발생:', error);
  }
};

  // 사용 패턴 데이터 가져오기
  const fetchUsagePatterns = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/user/usage-patterns`, {
      headers: {
        Authorization: `Bearer ${API_TOKEN}`,
      },
    });

    if (response.ok) {
      const rawData = await response.json();

      // 각 패턴 객체에 logoUrl 추가
      usagePatterns = rawData.map((pattern) => ({
        ...pattern,
        logoUrl: getLogoUrl(pattern.service_name),
      }));
    } else {
      console.error('사용 패턴 데이터를 가져오는데 실패했습니다.');
    }
  } catch (error) {
    console.error('사용 패턴 데이터 가져오기 중 오류 발생:', error);
  }
};
  // 정렬 기준과 순서 상태 변수 추가
  let sortKey = 'usage_percentage'; // 기본 정렬 기준
  let sortOrder = 'desc'; // 'asc' 또는 'desc'로 정렬 순서 지정

  // 정렬된 데이터를 저장할 변수
  let sortedUsageAnalysis = [];
  let sortedUsagePatterns = [];

  // 정렬 함수
  const sortData = () => {
    sortedUsageAnalysis = [...usageAnalysis].sort((a, b) => {
      if (sortOrder === 'asc') {
        return a[sortKey] - b[sortKey];
      } else {
        return b[sortKey] - a[sortKey];
      }
    });
  };

  // 정렬 기준 변경 함수
  const changeSortKey = (key) => {
    if (sortKey === key) {
      // 동일한 키를 클릭하면 정렬 순서 변경
      sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
      // 다른 키를 클릭하면 정렬 기준 변경
      sortKey = key;
      sortOrder = 'desc'; // 새로운 키로 변경 시 기본은 내림차순
    }
    sortData();
  };

  onMount(async () => {
    if (!API_TOKEN) {
      alert('로그인이 필요합니다.');
      goto('/login');
      return;
    }

    await fetchUsageAnalysis();
    await fetchUsagePatterns();

    sortData(); // 데이터 로드 후 정렬
  });

  function getLogoUrl(serviceName) {
  const logoMap = {
    "넷플릭스": "/images/netflix.png",
    "애플뮤직": "/images/applemusic.png",
    "스포티파이": "/images/spotify.png",
    "디즈니+":"/images/disney.png",
    "유튜브프리미엄":"/images/youtube.png"
  };
  return logoMap[serviceName] || "/images/default.png"; // 매핑되지 않은 서비스는 기본 로고 사용
}
</script>

<main class="analysis-page">
  <section class="usage-analysis">
    <h1>구독 효율성 분석</h1>

  <!-- 정렬 기준 선택 버튼 -->
  <div class="sort-buttons">
    <button on:click={() => changeSortKey('usage_percentage')}>
      사용 비율 {sortKey === 'usage_percentage' ? (sortOrder === 'asc' ? '▲' : '▼') : ''}
    </button>
    <button on:click={() => changeSortKey('cost_per_use')}>
      1회당 비용 {sortKey === 'cost_per_use' ? (sortOrder === 'asc' ? '▲' : '▼') : ''}
    </button>
    <!-- 다른 정렬 기준이 있으면 추가 -->
  </div>

  {#if sortedUsageAnalysis.length > 0}
    {#each sortedUsageAnalysis as analysis}
      <div class="analysis-item">
        <!-- 기존의 분석 아이템 표시 -->
        <div class="analysis-header">
          <img src={analysis.logoUrl} alt="{analysis.service_name} 로고" class="analysis-logo" />
          <h2>{analysis.service_name}</h2>
        </div>
        <p>갱신 간격: {analysis.total_days}일</p>
        <p>기간 내 사용 일수: {analysis.used_days}일</p>
        <p>사용 비율: {analysis.usage_percentage.toFixed(2)}%</p>
        <p>1회당 비용: {analysis.cost_per_use ? `${analysis.cost_per_use.toFixed(2)}원` : '정보 없음'}</p>
      </div>
    {/each}
  {:else}
    <p>사용 효율성 분석 데이터가 없습니다.</p>
  {/if}
  </section>

  <section class="usage-patterns">
    <h1>사용 패턴 분석</h1>
    {#if usagePatterns.length > 0}
      {#each usagePatterns as pattern}
        <div class="pattern-item">
          <div class="pattern-header">
            <img src={pattern.logoUrl} alt="{pattern.service_name} 로고" class="pattern-logo" />
            <h2>{pattern.service_name}</h2>
          </div>
          <p>총 사용 일수: {pattern.total_used_days}일</p>
          <p>하루에 몇 번?: {pattern.daily_average.toFixed(2)}번</p>
          <p>한 주에 몇 번?: {pattern.weekly_average.toFixed(2)}번</p>
          <p>한 달에 몇 번?: {pattern.monthly_average.toFixed(2)}번</p>
          <p>마지막 사용 날짜: {pattern.last_used_date ? pattern.last_used_date : '정보 없음'}</p>
          <p>가장 많이 사용하는 요일: {pattern.most_used_weekday ? pattern.most_used_weekday : '정보 없음'}</p>
        </div>
      {/each}
    {:else}
      <p>사용 패턴 데이터가 없습니다.</p>
    {/if}
  </section>
</main>

<style>
  .analysis-page {
    padding: 1rem;
    background-color: #000;
    color: #fff;
  }

  h1 {
    font-size: 30px;
    margin-bottom: 1rem;
  }

  .analysis-item, .pattern-item {
    background-color: #1e1e1e;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 8px;
  }

  h2 {
    font-size: 20px;
    margin-bottom: 0.5rem;
  }

  p {
    margin: 0.25rem 0;
  }
  .analysis-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
  }

  .analysis-logo {
    width: 40px;
    height: 40px;
    margin-right: 1rem;
  }

  .analysis-item h2 {
    margin: 0;
  }
  .pattern-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
  }

  .pattern-logo {
    width: 40px;
    height: 40px;
    margin-right: 1rem;
  }

  .pattern-item h2 {
    margin: 0;
  }
  .sort-buttons {
    margin-bottom: 1rem;
  }

  .sort-buttons button {
    background-color: #333;
    color: #fff;
    border: none;
    padding: 0.5rem 1rem;
    margin-right: 0.5rem;
    border-radius: 4px;
    cursor: pointer;
  }

  .sort-buttons button:hover {
    background-color: #555;
  }
</style>