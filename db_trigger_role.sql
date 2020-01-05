use shutongflow
DELIMITER //
CREATE TRIGGER role_trigger AFTER INSERT ON role FOR EACH ROW
BEGIN
INSERT INTO loonflow.account_loonrole(id,name,description,label,creator,gmt_created,gmt_modified,is_deleted) VALUES(new.id,new.name,new.description,'','admin',new.created,new.modified, new.deleted);
END//

CREATE TRIGGER role_trigger_update AFTER UPDATE ON role FOR EACH ROW
BEGIN
UPDATE loonflow.account_loonrole SET name = new.name where id=new.id;
UPDATE loonflow.account_loonrole SET description = new.description where id=new.id;
UPDATE loonflow.account_loonrole SET gmt_modified = new.modified where id=new.id;
UPDATE loonflow.account_loonrole SET is_deleted = new.deleted where id=new.id;
END//

CREATE TRIGGER role_del_trigger AFTER DELETE ON role FOR EACH ROW
BEGIN
DELETE FROM loonflow.account_loonrole WHERE id=old.id;
END//

CREATE TRIGGER user_role_trigger AFTER INSERT ON account_shutonguserrole FOR EACH ROW
BEGIN
INSERT INTO loonflow.account_loonuserrole(id,creator,gmt_created,gmt_modified,is_deleted,user_id,role_id) VALUES(new.id,'admin',new.created,new.modified,new.deleted,new.user,new.role);
END//

CREATE TRIGGER user_role_trigger_update AFTER UPDATE ON account_shutonguserrole FOR EACH ROW
BEGIN
UPDATE loonflow.account_loonuserrole SET user_id = new.user where id=new.id;
UPDATE loonflow.account_loonuserrole SET role_id = new.role where id=new.id;
UPDATE loonflow.account_loonuserrole SET gmt_modified = new.modified where id=new.id;
UPDATE loonflow.account_loonuserrole SET is_deleted = new.deleted where id=new.id;
END//

CREATE TRIGGER user_role_del_trigger AFTER DELETE ON account_shutonguserrole FOR EACH ROW
BEGIN
DELETE FROM loonflow.account_loonuserrole WHERE id=old.id;
END//


DELIMITER ;
