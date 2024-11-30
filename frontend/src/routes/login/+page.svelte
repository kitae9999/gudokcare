<script>
  import { goto } from "$app/navigation";

  let email = "";
  let password = "";
  let showPassword = false;

  const togglePasswordVisibility = () => {
      showPassword = !showPassword;
  };

  const handleLogin = async () => {
    if (!email || !password) {
        alert("아이디와 비밀번호를 입력해주세요.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem("token", data.access_token);

            // 토큰 디코딩하여 user_id 저장
            const tokenPayload = JSON.parse(atob(data.access_token.split(".")[1]));
            localStorage.setItem("user_id", tokenPayload.user_id);

            alert("로그인 성공!");
            goto("/main");
        } else {
            const errorData = await response.json();
            alert(`로그인 실패: ${errorData.detail}`);
        }
    } catch (error) {
        console.error("로그인 요청 중 오류 발생:", error);
        alert("서버와의 연결에 문제가 발생했습니다.");
    }
};

  const goToSignup = () => {
      goto("/signup"); // 회원가입 페이지로 이동
  };
</script>

<main class="login-page">
  <div class="login-container">
      <h1>로그인</h1>
      <div class="form-group">
          <label for="email">이메일</label>
          <input
              id="email"
              type="text"
              bind:value={email}
              placeholder="이메일을 입력해주세요"
          />
      </div>
      <div class="form-group">
          <label for="password">비밀번호</label>
          <div class="password-container">
              <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  bind:value={password}
                  placeholder="비밀번호를 입력해주세요"
              />
              <button
                  type="button"
                  class="toggle-password"
                  on:click={togglePasswordVisibility}
              >
                  {#if showPassword} 🔓 {:else} 🔒 {/if}
              </button>
          </div>
      </div>
      <div class="form-footer">
          <p>계정이 없으신가요? <a href="/signup">가입하기</a></p>
      </div>
      <button class="login-button" on:click={handleLogin}>로그인하기</button>
  </div>
</main>

<style>
  .login-page {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background-color: #000000;
      color: white;
  }

  .login-container {
      width: 90%;
      max-width: 400px;
      background: #1e1e1e;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  }

  h1 {
      text-align: center;
      margin-bottom: 20px;
      font-size: 24px;
  }

  .form-group {
      margin-bottom: 15px;
  }

  label {
      display: block;
      margin-bottom: 5px;
      font-size: 14px;
      color: #aaa;
  }

  input {
      width: 100%;
      padding: 10px;
      font-size: 14px;
      border: 1px solid #333;
      border-radius: 4px;
      background: #2c2c2c;
      color: white;
  }

  input::placeholder {
      color: #666;
  }

  .password-container {
      position: relative;
  }

  .toggle-password {
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: #666;
      cursor: pointer;
  }

  .form-footer {
      text-align: center;
      margin: 15px 0;
      font-size: 14px;
  }

  .form-footer a {
      color: #1e90ff;
      text-decoration: none;
      font-weight: bold;
  }

  .login-button {
      width: 100%;
      padding: 10px;
      font-size: 16px;
      background-color: #1e90ff;
      border: none;
      border-radius: 4px;
      color: white;
      cursor: pointer;
  }

  .login-button:hover {
      background-color: #1e90ff;
  }
</style>