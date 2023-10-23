use multi;

CREATE TABLE `NCS_code_info` (
	`NCS_code`	int	NOT NULL,
	`code1`	varchar(50)	NULL,
	`code2`	varchar(50)	NULL,
	`code3`	varchar(50)	NULL,
	`code4`	varchar(50)	NULL
);

CREATE TABLE `education` (
	`no`	int auto_increment	NOT NULL,
	`NCS_code`	int	NOT NULL,
	`train_title`	varchar(100)	NULL,
	`start_date`	date	NULL,
	`end_date`	date	NULL,
	`train_cost`	int	NULL,
	`target_people`	varchar(15)	NULL,
	`quota`	int	NULL,
	`link`	varchar(255)	NULL,
    `center_no` BIGINT,
    constraint `PK_EDUCATION` primary key (no)
);

CREATE TABLE `emp_prediction` (
	`no`	int auto_increment	NOT NULL,
	`date`	int	NULL,
	`city`	varchar(10)	NULL,
	`industry`	varchar(50)	NULL,
	`job_offer`	int	NULL,
	`job_search`	int	NULL,
	`no_company`	int	NULL,
	`unemployment`	int	NULL,
	`population`	int	NULL,
	`GDP`	decimal(8)	NULL,
	`i_rate`	decimal(8)	NULL,
	`CLI`	decimal(8)	NULL,
	`CFI`	decimal(8)	NULL,
    constraint `PK_EMP_PREDICION` primary key (no)
);

CREATE TABLE `emp_info` (
	`no`	int auto_increment	NOT NULL,
	`company`	varchar(50)	NULL,
	`job_name`	varchar(30)	NOT NULL,
	`city`	varchar(10)	NULL,
	`NCS_code`	int	NOT NULL,
	`stack`	varchar(30)	NULL,
	`link`	varchar(255)	NULL,
    constraint `PK_EMP_INFO` primary key (no)
);

CREATE TABLE `NCS_jobname` (
	`job_name`	varchar(30)	NOT NULL,
	`NCS_code`	int	NOT NULL
);

CREATE TABLE `education_center` (
    `center_no` BIGINT NOT NULL,
	`train_center`	varchar(30)	NOT NULL,
	`address`	varchar(20)	NULL,
	`center_tel`	varchar(13)	NULL,
    CONSTRAINT `PK_EDUCATION_CENTER` PRIMARY KEY (center_no)
);

CREATE TABLE `use_service` (
	`user_id`	varchar(255)	NOT NULL,
	`service_code`	int	NULL,
	`city`	varchar(10)	NULL,
	`industry`	varchar(30)	NULL,
	`job_name`	varchar(10)	NULL,
	`use_date`	date	NULL
);

CREATE TABLE `prediction_result` (
	`no`	int auto_increment	NOT NULL,
	`date`	int	NULL,
	`city`	varchar(10)	NULL,
	`industry`	varchar(50)	NULL,
	`result`	decimal(15)	NULL,
	`user_id`	varchar(300)	NULL,
    constraint `PK_PREDICTION_RESULT` primary key (no)
);

ALTER TABLE `NCS_code_info` ADD CONSTRAINT `PK_NCS_CODE_INFO` PRIMARY KEY (
	`NCS_code`
);

ALTER TABLE `education` ADD CONSTRAINT `FK_NCS_code_info_TO_education_1` FOREIGN KEY (
	`NCS_code`
)
REFERENCES `NCS_code_info` (
	`NCS_code`
);

ALTER TABLE `education` ADD CONSTRAINT `FK_education_center_TO_education_1` FOREIGN KEY (
	`center_no`
)
REFERENCES `education_center` (
	`center_no`
);

ALTER TABLE `NCS_jobname` ADD CONSTRAINT `FK_NCS_code_info_TO_NCS_jobname_1` FOREIGN KEY (
	`NCS_code`
)
REFERENCES `NCS_code_info` (
	`NCS_code`
);

-- 데이터 넣은 후 코드 실행하세요!
ALTER TABLE `emp_info` ADD CONSTRAINT `FK_NCS_jobname_TO_emp_info_1` FOREIGN KEY (
	`NCS_code`
)
REFERENCES `NCS_code_info` (
	`NCS_code`
);