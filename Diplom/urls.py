import enum


class URLS(enum.StrEnum):
    BASE = "https://opensource-demo.orangehrmlive.com/web/index.php/"
    LOGIN = BASE + "auth/login"
    PASSWORD = BASE + "auth/requestPasswordResetCode"
    DASHBOARD = BASE + "dashboard/index"
    ADMIN = BASE + "admin/viewSystemUsers"
    ADMIN_SAVE = BASE + "admin/saveSystemUser"
    PIM = BASE + "pim/viewEmployeeList"
    LEAVE = BASE + "leave/viewLeaveList"
    TIME = BASE + "time/viewEmployeeTimesheet/"
    RECRUITMENT = BASE + "/time/viewEmployeeTimesheet"
    MYINFO = BASE + "pim/viewPersonalDetails/empNumber/7"
    PERFORMANCE = BASE + "performance/searchEvaluatePerformanceReview"
    DIRECTORY = BASE + "directory/viewDirectory"
    MAINTENANCE = BASE + "maintenance/purgeEmployee"
    CLAIM = BASE + "claim/viewAssignClaim"
    BUZZ = BASE + "buzz/viewBuzz"
    RESET = BASE + "auth/requestPasswordResetCode"
