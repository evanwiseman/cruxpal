# backend/app/core/endpoints.py
from backend.app.core.config import settings


class APIEndpoints:
    """Centralized API endpoint paths"""

    # Base prefix
    API_V1_PREFIX = settings.API_V1_PREFIX

    # =======================
    # Auth
    # =======================
    AUTH_BASE = f"{API_V1_PREFIX}/auth"

    class AuthRoutes:
        LOGIN = "/login"
        SIGNUP = "/signup"
        REFRESH = "/refresh"
        ME = "/me"
        DEBUG_TOKEN = "/debug-token"

    # Full paths
    AUTH_LOGIN = f"{AUTH_BASE}{AuthRoutes.LOGIN}"
    AUTH_SIGNUP = f"{AUTH_BASE}{AuthRoutes.SIGNUP}"
    AUTH_REFRESH = f"{AUTH_BASE}{AuthRoutes.REFRESH}"
    AUTH_ME = f"{AUTH_BASE}{AuthRoutes.ME}"
    AUTH_DEBUG_TOKEN = f"{AUTH_BASE}{AuthRoutes.DEBUG_TOKEN}"

    # =======================
    # Ascents
    # =======================
    ASCENTS_BASE = f"{API_V1_PREFIX}/ascents"

    class AscentsRoutes:
        LIST = "/"
        CREATE = "/"
        GET_BY_ID = "/{ascent_id}"
        UPDATE = "/{ascent_id}"
        DELETE = "/{ascent_id}"

    # Full paths
    ASCENTS_LIST = f"{ASCENTS_BASE}{AscentsRoutes.LIST}"
    ASCENTS_CREATE = f"{ASCENTS_BASE}{AscentsRoutes.CREATE}"
    ASCENTS_GET_BY_ID = f"{ASCENTS_BASE}{AscentsRoutes.GET_BY_ID}"
    ASCENTS_UPDATE = f"{ASCENTS_BASE}{AscentsRoutes.UPDATE}"
    ASCENTS_DELETE = f"{ASCENTS_BASE}{AscentsRoutes.DELETE}"

    # =======================
    # ATHLETES
    # =======================
    ATHLETES_BASE = f"{API_V1_PREFIX}/athletes"

    class AthletesRoutes:
        LIST = "/"
        CREATE = "/"
        GET_BY_ID = "/{athlete_id}"
        LIST_ASCENTS = "/{athlete_id}/ascents"
        LIST_ROUTES = "/{athlete_id}/routes"
        UPDATE = "/{athlete_id}"
        DELETE = "/{athlete_id}"

    # Full paths
    ATHLETES_LIST = f"{ATHLETES_BASE}{AthletesRoutes.LIST}"
    ATHLETES_CREATE = f"{ATHLETES_BASE}{AthletesRoutes.CREATE}"
    ATHLETES_GET_BY_ID = f"{ATHLETES_BASE}{AthletesRoutes.GET_BY_ID}"
    ATHLETES_LIST_ASCENTS = f"{ATHLETES_BASE}{AthletesRoutes.LIST_ASCENTS}"
    ATHLETES_LIST_ROUTES = f"{ATHLETES_BASE}{AthletesRoutes.LIST_ROUTES}"
    ATHLETES_UPDATE = f"{ATHLETES_BASE}{AthletesRoutes.UPDATE}"
    ATHLETES_DELETE = f"{ATHLETES_BASE}{AthletesRoutes.DELETE}"

    # =======================
    # Routes
    # =======================
    ROUTES_BASE = f"{API_V1_PREFIX}/ROUTES"

    class RoutesRoutes:
        LIST = "/"
        CREATE = "/"
        GET_BY_ID = "/{route_id}"
        LIST_ATHLETES = "/{route_id}/athletes"
        UPDATE = "/{route_id}"
        DELETE = "/{route_id}"

    # Full paths
    ROUTES_LIST = f"{ROUTES_BASE}{RoutesRoutes.LIST}"
    ROUTES_CREATE = f"{ROUTES_BASE}{RoutesRoutes.CREATE}"
    ROUTES_GET_BY_ID = f"{ROUTES_BASE}{RoutesRoutes.GET_BY_ID}"
    ROUTES_LIST_ATHLETES = f"{ROUTES_BASE}{RoutesRoutes.LIST_ATHLETES}"
    ROUTES_UPDATE = f"{ROUTES_BASE}{RoutesRoutes.UPDATE}"
    ROUTES_DELETE = f"{ROUTES_BASE}{RoutesRoutes.DELETE}"


endpoints = APIEndpoints()
