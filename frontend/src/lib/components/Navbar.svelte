<script>
    import { goto } from "$app/navigation";
  
    const goToAddSubscription = () => {
      goto("/add-subscription");
    };
  
    const goToNotifications = () => {
      alert("알림 기능은 아직 구현되지 않았습니다!"); // 추후 알림 기능 추가
    };
  </script>
  <p></p>
  <nav class="navbar">
    <button class="icon-button" on:click={goToAddSubscription}>
        <svg xmlns="http://www.w3.org/2000/svg" width="34" height="36" viewBox="0 0 34 36" fill="none">
            <path d="M19.4148 5.625C19.4148 4.38047 18.3356 3.375 17 3.375C15.6643 3.375 14.5852 4.38047 14.5852 5.625V15.75H3.71873C2.38306 15.75 1.30396 16.7555 1.30396 18C1.30396 19.2445 2.38306 20.25 3.71873 20.25H14.5852V30.375C14.5852 31.6195 15.6643 32.625 17 32.625C18.3356 32.625 19.4148 31.6195 19.4148 30.375V20.25H30.2812C31.6169 20.25 32.696 19.2445 32.696 18C32.696 16.7555 31.6169 15.75 30.2812 15.75H19.4148V5.625Z" fill="white"/>
          </svg>
    </button>
    <button class="icon-button" on:click={goToNotifications}>
        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" fill="none">
            <path d="M32.4 29.8688L31.275 28.125C31.05 27.7875 30.9375 27.45 30.9375 27.0563V15.3563C30.9375 12.0375 29.5312 8.9438 26.9437 6.63755C24.8625 4.7813 22.1625 3.60005 19.2937 3.37505V2.25005C19.2937 1.57505 18.7312 0.956299 18 0.956299C17.325 0.956299 16.7062 1.5188 16.7062 2.25005V3.3188C16.5937 3.3188 16.4812 3.3188 16.3687 3.37505C9.84374 4.1063 4.94999 9.33755 4.94999 15.5813V27.0563C4.89374 27.6188 4.78124 27.9 4.66874 28.0688L3.59999 29.8688C3.26249 30.4313 3.26249 31.1063 3.59999 31.6688C3.93749 32.175 4.49999 32.5125 5.11874 32.5125H16.7625V33.75C16.7625 34.425 17.325 35.0438 18.0562 35.0438C18.7312 35.0438 19.35 34.4813 19.35 33.75V32.5125H30.9375C31.5562 32.5125 32.1187 32.175 32.4562 31.6688C32.7937 31.1063 32.7937 30.4313 32.4 29.8688ZM6.46874 29.9813L6.86249 29.3063C7.19999 28.7438 7.36874 28.0688 7.48124 27.2813V15.5813C7.48124 10.6313 11.4187 6.4688 16.65 5.9063C19.8562 5.5688 23.0062 6.52505 25.3125 8.55005C27.3375 10.35 28.4625 12.7688 28.4625 15.3563V27.0563C28.4625 27.9 28.6875 28.6876 29.1937 29.475L29.5312 29.9813H6.46874Z" fill="white"/>
          </svg>
    </button>
  </nav>
  
  <style>
    .navbar {
  width: 100%; /* 너비를 전체 화면 기준으로 설정 */
  max-width: 335px; /* 최대 너비를 설정하여 중앙에서 고정 */
  height: 37px;
  display: flex;
  justify-content: space-between; /* 아이템을 양쪽 끝으로 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
  background-color: #000000;
  color: white;
  padding: 0 1rem; /* 양쪽 여백만 추가 */
  margin: 0 auto; /* navbar를 화면 가운데로 정렬 */
}

.icon-button {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.icon-button:hover {
  color: #63b3ed;
}
  </style>