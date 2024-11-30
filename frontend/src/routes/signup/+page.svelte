<script>
    import { goto } from '$app/navigation';

    let email = '';
    let password = '';
    let confirmPassword = '';

    const handleSignup = async () => {
        if (password !== confirmPassword) {
            alert('비밀번호가 일치하지 않습니다.');
            return;
        }

        try {
            // API 요청
            const response = await fetch('http://127.0.0.1:8000/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                // 서버에서 받은 에러 메시지 출력
                const error = await response.json();
                alert(`회원가입 실패: ${error.detail}`);
                return;
            }

            alert('회원가입 성공!');
            // 로그인 페이지로 이동
            goto('/login');
        } catch (error) {
            console.error('회원가입 요청 중 오류 발생:', error);
            alert('회원가입 요청 중 문제가 발생했습니다.');
        }
    };
</script>

<main class="signup-container">
    <div class="signup-box">
        <h1>회원가입</h1>

        <div class="form-group">
            <label for="email">이메일</label>
            <input
                id="email"
                type="email"
                placeholder="이메일을 입력해주세요"
                bind:value={email}
            />
        </div>

        <div class="form-group">
            <label for="password">비밀번호</label>
            <input
                id="password"
                type="password"
                placeholder="비밀번호를 입력해주세요"
                bind:value={password}
            />
        </div>

        <div class="form-group">
            <label for="confirm-password">비밀번호 확인</label>
            <input
                id="confirm-password"
                type="password"
                placeholder="비밀번호를 다시 입력해주세요"
                bind:value={confirmPassword}
            />
        </div>

        <button class="signup-button" on:click={handleSignup}>회원가입하기</button>

        <p class="login-redirect">
            이미 계정이 있으신가요? <a href="/login">로그인</a>
        </p>
    </div>
</main>

<style>
    .signup-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #000;
        color: white;
    }

    .signup-box {
        background-color: #1c1c1c;
        padding: 2rem;
        border-radius: 10px;
        width: 90%;
        max-width: 400px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    .signup-box h1 {
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .form-group {
        margin-bottom: 1rem;
        text-align: left;
    }

    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
    }

    .form-group input {
        width: 100%;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #333;
        background-color: #2c2c2c;
        color: white;
        font-size: 0.875rem;
    }

    .form-group input::placeholder {
        color: #666;
    }

    .signup-button {
        width: 100%;
        padding: 0.75rem;
        background-color: #1e90ff;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 1rem;
        cursor: pointer;
    }

    .signup-button:hover {
        background-color: #1c86ee;
    }

    .login-redirect {
        margin-top: 1rem;
        font-size: 0.875rem;
    }

    .login-redirect a {
        color: #1e90ff;
        text-decoration: none;
    }

    .login-redirect a:hover {
        text-decoration: underline;
    }
</style>