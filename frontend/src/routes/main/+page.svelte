<script>
    import SubscriptionItem from "$lib/components/SubscriptionItem.svelte";
    import { subscriptions, fetchSubscriptionsFromAPI } from "$lib/stores/subscriptions";
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import { goto } from "$app/navigation";

    // 구독료 총합 저장용 스토어
    const totalCost = writable(0);

    // API URL 설정
    const API_BASE_URL = "http://127.0.0.1:8000/contracts";
    const API_TOKEN = localStorage.getItem("token");

    // 총 구독료 가져오기
    const fetchTotalCost = async () => {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch(`${API_BASE_URL}/user/contracts/total-cost`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                totalCost.set(data); // 스토어 업데이트
            } else {
                alert("구독료 총합을 가져오는데 실패했습니다.");
            }
        } catch (error) {
            console.error("구독료 총합 가져오기 중 오류 발생:", error);
        }
    };

    // 특정 구독 삭제
const deleteSubscription = async (id) => {  
    try {
        const token = localStorage.getItem("token");
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (response.ok) {
            subscriptions.update((subs) => subs.filter((sub) => sub.id !== id));
            alert("구독이 성공적으로 삭제되었습니다.");
            await fetchTotalCost(); // 구독 삭제 후 총합 업데이트
        } else {
            const errorData = await response.json();
            alert(`구독 삭제에 실패했습니다: ${errorData.detail}`);
        }
    } catch (error) {
        console.error("구독 삭제 중 오류 발생:", error);
        alert("구독 삭제 중 오류가 발생했습니다.");
    }
};

    // 구독 상태 토글 (usedToday를 반영)
    const toggleUsage = async (id, used) => {
    try {
        const token = localStorage.getItem("token");
        const response = await fetch(`${API_BASE_URL}/${id}/log-usage?used=${used}`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (response.ok) {
            alert("사용 기록이 업데이트되었습니다.");
        } else {
            alert("사용 기록 업데이트에 실패했습니다.");
        }
    } catch (error) {
        console.error("사용 기록 업데이트 중 오류 발생:", error);
    }
};

    // 컴포넌트가 마운트될 때 실행
    onMount(async () => {
        if (!API_TOKEN) {
            alert("로그인이 필요합니다.");
            goto("/login");
            return;
        }

        await fetchSubscriptionsFromAPI(API_TOKEN); // API 호출로 구독 데이터 가져오기
        await fetchTotalCost(); // 총 구독료 가져오기
    });
</script>

<main class="home">
    <header class="header">
        <h1 class="header-title">나의 구독료 총 합</h1>
        <div class="total-cost-container">
            <p class="total-cost">{`${$totalCost.toLocaleString()}원`}</p>
        </div>
    </header>

    <section class="subscription-list">
        <h2 class="subscription-list-title">나의 구독목록</h2>
        {#each $subscriptions as subscription}
            <SubscriptionItem
            {subscription}
            class="subscription-item"
            on:toggleUsage={(event) => toggleUsage(event.detail.id, event.detail.used)}
            on:delete={() => deleteSubscription(subscription.id)}
        />
        {/each}
    </section>
</main>

<style>
    .home {
        display: flex;
        flex-direction: column;
        background-color: #000000;
        color: white;
        min-height: 100vh;
        padding: 1rem;
    }

    .header {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .header-title {
        text-align: left;
        font-size: 30px;
        margin: 0;
        padding-bottom: 10px;
    }

    .total-cost-container {
        width: 100%;
        text-align: center;
        margin-top: 0.5rem;
    }

    .total-cost {
        font-size: 24px;
        font-weight: bold;
        color: #007aff;
        margin: 0;
    }

    .subscription-list {
        margin-top: 3rem;
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