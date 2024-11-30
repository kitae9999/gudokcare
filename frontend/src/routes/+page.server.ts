import { redirect } from "@sveltejs/kit";

export const load = async () => {
    // 루트 경로로 접속하면 `/login`으로 리다이렉트
    throw redirect(302, "/login");
};