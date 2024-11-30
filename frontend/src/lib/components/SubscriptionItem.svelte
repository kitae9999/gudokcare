<script>
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
    export let subscription;
  
  
    const getDaysLeftClass = (daysLeft) => {
      if (daysLeft <= 7) {
        return "days-left-danger";
      } else if (daysLeft > 7 && daysLeft <= 14) {
        return "days-left-warning";
      } else {
        return "days-left-safe";
      }
    };
    const handleDelete = () => {
      dispatch('delete', { id: subscription.id });
    };

    let isToggled = subscription.usedToday;
    const toggle = () => {
    isToggled = !isToggled;
    dispatch('toggleUsage', { id: subscription.id, used: isToggled });
  };
    
  </script>
  
  <div class="subscription-item">
    <!-- 왼쪽 영역 -->
    <div class="subscription-logo">
      <img src="{subscription.logoUrl}" alt="{subscription.name} 로고" class="logo-image" />
    </div>
  
    <!-- 중간 영역 -->
    <div class="subscription-details">
      <h3>{subscription.name}</h3>
      <p class={`days-left ${getDaysLeftClass(subscription.daysLeft)}`}>D-{subscription.daysLeft}</p>
    </div>
  
    <!-- 오른쪽 영역 -->
    <div class="subscription-actions">
      <div class="top-row">
        <!-- 토글 스위치 -->
        <label class="toggle-switch">
          <input type="checkbox" checked={isToggled} on:change={toggle} />
          <span class="slider"></span>
        </label>
  
        <!-- 삭제 버튼 -->
        <button class="delete-button" on:click={handleDelete}>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="22" viewBox="0 0 20 22" fill="none">
            <path
              d="M16 20H4V6H2V19.7C2 20.8 2.9 22 4 22H16C17.1 22 18 20.8 18 19.7V6H16V20ZM13 2V0H7V2H0V4H20V2H13ZM7 8V18H9V8H7ZM11 8V18H13V8H11Z"
              fill="white"
            />
          </svg>
        </button>
      </div>
  
      <!-- 가격 -->
      <p class="price">{subscription.price.toLocaleString()}원 / 월</p>
    </div>
  </div>
  
  <style>
    .subscription-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top : 1rem;
      margin-bottom: 1.5rem;
      background-color: #000;
      color: white;
      border-radius: 8px;
    }
  
    .subscription-logo img {
      height: 52px;
      object-fit: cover;
    }
  
    .subscription-details {
      flex-grow: 1;
      padding: 0 1rem;
    }
  
    .subscription-details h3 {
      margin: 0;
      font-family: "SF Pro";
      font-size: 24px;
      font-weight: bold;
    }
  
    .days-left {
      margin: 0;
      font-family: "SF Pro";
      font-size: 14px;
      font-weight: bold;
      line-height: normal;
    }
  
    /* 7일 이하 */
    .days-left-danger {
      color: #9c1e1e;
    }
  
    /* 7초과 14이하 */
    .days-left-warning {
      color: #8f4949;
    }
  
    /* 14초과 */
    .days-left-safe {
      color: #746868;
    }
  
    .subscription-actions {
      display: flex;
      flex-direction: column; /* 세로 정렬 */
      align-items: flex-end; /* 오른쪽 정렬 */
      gap: 0.5rem; /* 위아래 간격 */
    }
  
    .top-row {
      display: flex;
      align-items: center; /* 수직 중앙 정렬 */
      gap: 1.1rem; /* 토글과 삭제 버튼 사이 간격 */
    }
  
    /* 토글 스위치 스타일 */
    .toggle-switch {
      position: relative;
      display: inline-block;
      width: 40px;
      height: 20px;
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
      height: 14px;
      width: 14px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      transition: 0.4s;
      border-radius: 50%;
    }
  
    input:checked + .slider {
      background-color: #2196f3;
    }
  
    input:checked + .slider:before {
      transform: translateX(20px);
    }
  
    .delete-button {
      background: none;
      border: none;
      cursor: pointer;
    }
  
    .delete-button svg {
      fill: white;
      transition: fill 0.3s ease;
    }
  
    .delete-button:hover svg {
      fill: #ff4d4f;
    }
  
    .price {
      font-family: "SF Pro";
      font-size: 14px;
      font-weight: bold;
      text-align: right;
    }
  </style>