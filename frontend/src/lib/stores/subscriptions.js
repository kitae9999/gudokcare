// import { writable } from "svelte/store";

// export const subscriptions = writable([
//   { id: 1, name: "넷플릭스", daysLeft: 7, price: 9900, usedToday: false,logoUrl:"/images/netflix.png"},
//   { id: 2, name: "애플뮤직", daysLeft: 13, price: 11000, usedToday: false,logoUrl:"/images/applemusic.png" },
//   { id: 3, name: "스포티파이", daysLeft: 21, price: 8700, usedToday: false ,logoUrl:"/images/spotify.png"},
// ]);
import { writable } from "svelte/store";

export const subscriptions = writable([]); // 초기값 빈 배열

export const fetchSubscriptionsFromAPI = async (token) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/contracts/user/contracts`, {
      headers: {
        Authorization: `Bearer ${token}`, // Bearer Token 방식 인증
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const rawData = await response.json();

      // 데이터를 변환하여 기존 형식에 맞춤
      const transformedData = rawData.map((item) => ({
        id: item.id,
        name: item.service_name,
        daysLeft: calculateDaysLeft(item.end_date), // 남은 일수 계산
        price: item.monthly_cost,
        usedToday: item.used_today,
        logoUrl: getLogoUrl(item.service_name), // 서비스 이름에 따른 로고 URL 지정
      }));

      subscriptions.set(transformedData); // 변환된 데이터를 스토어에 설정
    } else {
      console.error("구독 데이터를 가져오지 못했습니다.");
    }
  } catch (error) {
    console.error("구독 데이터 가져오기 실패:", error);
  }
};

// 남은 일수를 계산하는 함수
function calculateDaysLeft(endDate) {
  const end = new Date(endDate);
  const today = new Date();
  const diffTime = end - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays > 0 ? diffDays : 0; // 만료일이 지났다면 0 반환
}

// 서비스 이름에 따라 로고 URL을 매핑하는 함수
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