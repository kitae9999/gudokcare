<script>
    import Navbar from "$lib/components/Navbar.svelte";
    import '../app.css';
    import { page } from "$app/stores"; // 현재 경로 확인을 위해 import

    let hideNavigation = false;

    $: {
        // 특정 경로에서 상단바와 하단바를 숨김
        const hidePaths = ["/login", "/signup","/"]; // 숨기고 싶은 경로들
        hideNavigation = hidePaths.includes($page.url.pathname);
    }
</script>

<div class="layout">
    {#if !hideNavigation}
        <Navbar />
    {/if}

    <main>
        <slot />
    </main>

    {#if !hideNavigation}
        <nav class="bottom-nav">
            <a href="/main" class="nav-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
                </svg>
                <span>홈</span>
            </a>
            <a href="/statistics" class="nav-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M3 13h2v-2H3v2zm4 6h2v-8H7v8zm4-3h2v-5h-2v5zm4 7h2V8h-2v15zm4-12h2V3h-2v8z"/>
                </svg>
                <span>분석</span>
            </a>
        </nav>
    {/if}
</div>

<style>
    .layout {
        display: flex;
        flex-direction: column;
        background-color: #000000; /* 페이지 배경색 */
        color: white;
    }

    main {
        flex: 1; /* 남은 공간을 차지하도록 설정 */
        overflow-y: auto; /* 스크롤이 필요한 경우 세로로 스크롤 가능 */
        padding: 1rem; /* 내부 여백 추가 */
    }

    .bottom-nav {
        position: fixed; /* 하단에 고정 */
        bottom: 0;
        left: 0;
        width: 100%;
        height: 6rem; /* 하단바 높이 */
        background-color: #000; /* 배경색 */
        display: flex;
        justify-content: space-around; /* 아이템 간 간격 */
        align-items: center; /* 세로 정렬 */
        color: white; /* 텍스트 및 아이콘 색상 */
    }

    .nav-item {
        text-decoration: none; /* 링크 밑줄 제거 */
        color: white; /* 텍스트 색상 */
        font-size: 0.875rem; /* 텍스트 크기 */
        display: flex;
        flex-direction: column; /* 세로 정렬 */
        justify-content: center; /* 세로 가운데 정렬 */
        align-items: center; /* 중앙 정렬 */
        gap: 0.3rem; /* 아이콘과 텍스트 사이 간격 */
    }

    .nav-item svg {
        width: 30px; /* 아이콘 너비 */
        height: 30px; /* 아이콘 높이 */
        fill: currentColor; /* 아이콘 색상을 텍스트와 동일하게 설정 */
    }

    .nav-item:hover {
        color: #1e90ff; /* 호버 시 색상 변경 */
    }
</style>