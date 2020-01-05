use shutongflow;
DROP TRIGGER user_trigger;
DROP TRIGGER user_trigger_update;
DROP TRIGGER user_del_trigger;
DROP TRIGGER dept_trigger;
DROP TRIGGER dept_del_trigger;
DELIMITER //
CREATE TRIGGER user_trigger AFTER INSERT ON user FOR EACH ROW
BEGIN
INSERT INTO loonflow.account_loonuser(id,username,alias,email,password,phone,creator,dept_id,is_active,is_admin,is_deleted,gmt_created,gmt_modified) VALUES(new.id,new.username,new.alias,new.email,new.password,new.phone,'admin',new.dept,1,0,0,new.created, new.modified);
END//

CREATE TRIGGER user_trigger_update AFTER UPDATE ON user FOR EACH ROW
BEGIN
UPDATE loonflow.account_loonuser SET alias = new.alias where id=new.id;
UPDATE loonflow.account_loonuser SET email = new.email where id=new.id;
UPDATE loonflow.account_loonuser SET phone = new.phone where id=new.id;
UPDATE loonflow.account_loonuser SET dept_id = new.dept where id=new.id;
UPDATE loonflow.account_loonuser SET is_active = new.is_active where id=new.id;
UPDATE loonflow.account_loonuser SET is_admin = new.is_superuser where id=new.id;
END//

CREATE TRIGGER user_del_trigger AFTER DELETE ON user FOR EACH ROW
BEGIN
DELETE FROM loonflow.account_loonuser WHERE id=old.id;
END//

CREATE TRIGGER dept_trigger AFTER INSERT ON account_shutongdept FOR EACH ROW
BEGIN
INSERT INTO loonflow.account_loondept(id,name,parent_dept_id,leader,approver,label,creator,is_deleted,gmt_created,gmt_modified) VALUES(new.id,new.name,new.parent,new.leader,'','','',new.deleted,new.created, new.modified);
END//

CREATE TRIGGER dept_del_trigger AFTER DELETE ON account_shutongdept FOR EACH ROW
BEGIN
DELETE FROM loonflow.account_loondept WHERE id=old.id;
END//

DELIMITER ;
