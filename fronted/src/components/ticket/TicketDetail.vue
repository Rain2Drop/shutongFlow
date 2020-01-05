<template>
  <div class="wrapper">
    <!-- 流程图 -->
    <Row :gutter="10">
      <Col :md="{span: 24}">
        <Card style="text-align: left;">
          <template slot="title">
            <span style="font-weight: 700;">
              <Icon type="map"></Icon>
              <span>业务流程</span>
            </span>
          </template>
          <Steps :current="currentStep">
            <Step v-for="(step, index) in steps" :key="index" :title="step.state_name"></Step>
          </Steps>
        </Card>
      </Col>
    </Row>
    <!-- 详情与操作 -->
    <Row :gutter="1" style="text-align: left; margin: 5px 0;">
      <Col :md="{span: 24}">
        <Card id="ticket-detail">
          <template slot="title">
            <span style="font-weight: 700;">
              <Icon type="android-clipboard"></Icon>
              <span>{{workflow.name}}</span>
            </span>
          </template>
          <Row>
            <Form :model="detailForm" ref="detailForm" :rules="detailFormRules" :label-width="150">
              <Col
                v-for="(field, index) in shortFieldList"
                :key="index"
                :md="{span: field.field_type_id === 55 ? 22 : 11}"
              >
                <template v-if="/2|3/.test(field.field_attribute)">
                  <FormItem
                    v-if="field.field_type_id === 5"
                    :label="field.name || field.field_name"
                    :prop="field.field_key"
                  >
                    <Input
                      v-model="detailForm[field.field_key]"
                      :placeholder="$t(`field_label.${field.field_key}`)"
                    ></Input>
                  </FormItem>
                  <FormItem
                    v-else-if="field.field_type_id === 15"
                    :prop="field.field_key"
                    :label="field.name || field.field_name"
                  >
                    <InputNumber
                      v-model="detailForm[field.field_key]"
                      :min="0"
                      :step="0.5"
                      style="width: 100%;"
                    ></InputNumber>
                  </FormItem>
                  <FormItem
                    v-else-if="field.field_type_id === 30"
                    :prop="field.field_key"
                    :label="field.name || field.field_name"
                  >
                    <DatePicker
                      v-model="detailForm[field.field_key]"
                      type="datetime"
                      format="yyyy-MM-dd HH:mm:ss"
                      style="width: 100%;"
                      :placeholder="$t(`field_label.${field.field_key}`)"
                    ></DatePicker>
                  </FormItem>
                  <FormItem
                    v-else-if="field.field_type_id === 40"
                    :prop="field.field_key"
                    :label="field.name || field.field_name"
                  >
                    <Select
                      v-model="detailForm[field.field_key]"
                      multiple
                      :placeholder="$t(`field_label.${field.field_key}`)"
                    >
                      <Option
                        v-for="(choice, i) in Object.keys(field.field_choice)"
                        :key="i"
                        :value="choice"
                      >{{field.field_choice[choice]}}</Option>
                    </Select>
                  </FormItem>
                  <FormItem
                    v-else-if="[35, 45].includes(field.field_type_id)"
                    :prop="field.field_key"
                    :label="field.name || field.field_name"
                  >
                    <Select
                      v-model="detailForm[field.field_key]"
                      :placeholder="$t(`field_label.${field.field_key}`)"
                    >
                      <Option
                        v-for="(choice, i) in Object.keys(field.field_choice)"
                        :key="i"
                        :value="choice"
                      >{{field.field_choice[choice]}}</Option>
                    </Select>
                  </FormItem>
                  <FormItem
                    v-else-if="field.field_type_id === 60"
                    :prop="field.field_key"
                    :label="field.name || field.field_name"
                  >
                    <Select
                      v-model="detailForm[field.field_key]"
                      :placeholder="$t(`field_label.${field.field_key}`)"
                    >
                      <Option
                        v-for="(user, index) in accountList"
                        :key="index"
                        :value="user.username"
                      >{{user.alias}}</Option>
                    </Select>
                  </FormItem>
                  <FormItem
                    v-else-if="field.field_type_id === 55"
                    :prop="field.field_key"
                    :label="field.name || field.field_name"
                  >
                    <ueditor @ready="handleReady"></ueditor>
                  </FormItem>
                  <FormItem
                    v-else-if="field.field_type_id === 80"
                    :prop="field.field_key"
                    :label="field.name || field.field_name"
                  >
                    <el-upload
                      action="/api/v1/service/ueditor/?action=uploadfile&encode=utf-8"
                      :on-success="onsuccess"
                      :on-remove="onremove"
                      :on-preview="onpreview"
                      name="upfile"
                      :file-list="fileList">
                      <Button type="primary" size="small">点击上传</Button>
                    </el-upload>
                  </FormItem>
                  <FormItem
                    v-else-if="field.field_type_id === 90"
                    :prop="field.field_key"
                    :label="field.name || field.field_name"
                  >
                    <el-upload
                      action="/api/v1/service/ueditor/?action=uploadimage"
                      :on-success="imgOnsuccess"
                      :on-remove="imgOnremove"
                      :on-preview="function(){Dialog = true}"
                      accept="image/*"
                      name="upfile"
                      list-type="picture-card"
                      :file-list="imgFileList">
                      <i class="el-icon-plus"></i>
                    </el-upload>
                    <el-dialog
                      :visible.sync="Dialog" 
                      :modal="false"
                      top="10vh">
                      <img width="100%" :src="imgFileList[0] ? imgFileList[0].url : ''" alt="图片">
                    </el-dialog>
                  </FormItem>
                </template>
                <template v-else-if="field.field_attribute === 1">
                  <FormItem :label="field.name || field.field_name">
                    <div class="disabled_field" v-html="displaySelectKey(field)"></div>
                  </FormItem>
                </template>
              </Col>
              <Col :md="{span: 22}" v-if="transitions.length > 0">
                <FormItem label="处理意见" :prop="detailForm['suggestion']">
                  <Input type="textarea" v-model="suggestion" placeholder="请输入处理意见"></Input>
                </FormItem>
              </Col>
              <Col :md="{span: 24, offset: 2}">
                <Button
                  v-for="(btn, index) in transitions"
                  :key="index"
                  type="primary"
                  style="margin: 10px 10px;"
                  @click="handleTicketTransition('detailForm', btn)"
                >{{btn.transition_name}}</Button>
              </Col>
            </Form>
          </Row>
        </Card>
      </Col>
    </Row>
    <!-- 日志 -->
    <Row :gutter="10">
      <Col :md="{span: 24}">
        <Card style="text-align: left;">
          <template slot="title">
            <span style="font-weight: 700;">
              <Icon type="clipboard"></Icon>
              <span>操作日志</span>
            </span>
          </template>
          <Table :columns="logtable.columns" :data="logtable.data"></Table>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
import Utils from "../../utils";
import Validators from "../../utils/validators";
import { Date } from "../../utils/datetime";
import ueditor from './components/ueditor';

export default {
  name: "ticket-detail",
  data() {
    return {
      ticket: {},
      workflow: {},
      logtable: {
        columns: [
          {
            key: "state",
            title: "节点名称",
            align: "center",
            render: (h, params) => {
              return h("div", [h("span", {}, params.row.state.state_name)]);
            }
          },
          {
            key: "participant",
            title: "参与者",
            align: "center"
          },
          {
            key: "gmt_created",
            title: "操作时间",
            align: "center"
          },
          {
            key: "suggestion",
            title: "处理意见",
            align: "center",
            render: (h, params) => {
              return h("div", [
                h(
                  "span",
                  {},
                  params.row.suggestion ? params.row.suggestion : "——"
                )
              ]);
            }
          }
        ],
        data: []
      },
      accountList: [],
      steps: [],
      currentStep: 1,
      cardHeight: "",
      stepTransition: {},
      transitions: [],
      suggestion: "",
      detailForm: {},
      detailFormRules: {},
      fileList: [],
      imgFileList: [],
      Dialog: false
    };
  },
  components: {
    ueditor,
  },
  methods: {
    onsuccess(response, file, fileList) {
      if (response.state != 'SUCCESS') {
        this.$Notice.error({title: '上传失败'})
        this.fileList = []
      } else {
        this.fileList = [{
          name: file.name,
          url: response.url
        }]
        let item = this.shortFieldList.find(i => i.field_type_id === 80)
        this.detailForm[item.field_key] = response.url
      }
    },
    onremove (file, fileList) {
      let item = this.shortFieldList.find(i => i.field_type_id === 80)
      this.detailForm[item.field_key] = ''
    },
    imgOnsuccess (response, file, fileList) {
      console.log(response)
      if (response.state != 'SUCCESS') {
        this.$Notice.error({title: '上传失败'})
        this.imgFileList = []
      } else {
        this.imgFileList = [file]
        let item = this.shortFieldList.find(i => i.field_type_id === 90)
        this.detailForm[item.field_key] = response.url
      }
    },
    imgOnremove (file, fileList) {
      let item = this.shortFieldList.find(i => i.field_type_id === 90)
      this.detailForm[item.field_key] = ''
    },
    onpreview (file) {
      open(file.url)
    },
    handleReady (instance) {
      let field_key
      for (let i = 0; i < this.shortFieldList.length; i++) {
        if (this.shortFieldList[i].field_type_id === 55) {
          field_key = this.shortFieldList[i].field_key
        }
      }
      instance.setContent(this.detailForm[field_key] || '')
      instance.addListener('contentChange', () => {
        this.detailForm[field_key] = instance.getContent()
      })
    },
    init() {
      this.$store
        .dispatch("api_get_ticket_detail", { id: this.ticket_id })
        .then(resp => {
          this.ticket = resp.data.data.value;
          console.log(this.ticket)
          const workflow_id = this.ticket.workflow_id;
          this.$store.dispatch("api_workflows").then(resp => {
            let workflows = resp.data.data.value;
            this.workflow = workflows.filter(item => {
              if (item.id === workflow_id) {
                return true;
              }
            })[0];
          });
          this.$store
            .dispatch("api_get_ticket_transiton_list", { id: this.ticket.id })
            .then(resp => {
              this.logtable.data = resp.data.data.value;
            });
          this.$store
            .dispatch("api_get_ticket_step_list", { id: this.ticket.id })
            .then(resp => {
              this.steps = resp.data.data.value;
            });
          this.$store
            .dispatch("api_get_ticket_transitions", { id: this.ticket.id })
            .then(resp => {
              this.transitions = resp.data.data.value;
            })
            .catch(error => {
              this.$Notice.info({ title: "当前状态您无法处理该工单" });
            });
          this.$store.dispatch("api_fetch_account_list").then(resp => {
            this.accountList = resp.data.data;
          });
        })
        .catch(error => {
          this.$Notice.error({ title: "接口错误或数据不存在！" });
        });
    },
    submit(btn, data) {
      let p
      if(btn.is_accept) {
        p = this.$store.dispatch("api_post_ticket_accept", data)
      } else {
        p = this.$store.dispatch("api_handle_ticket_action", data)
      }
      p.then(resp => {
        this.$Notice.success({ title: "处理成功" });
        this.$router.push({ name: "todo" });
      })
      .catch(error => {
        this.$Notice.error({ title: "工单处理失败" });
        console.log(error);
      });
    },
    handleTicketTransition(formName, btn) {
      console.log(this.detailForm, this.detailFormRules, btn)
      this.$refs[formName].validate(valid => {
        if (valid) {
          console.log('btn',btn)
          let data = {
            id: this.ticket.id,
            data: {
              transition_id: btn.transition_id,
              suggestion: this.suggestion
                ? this.suggestion
                : btn.transition_name
            }
          };
          let formData = {};
          let detailFormKeys = Object.keys(this.detailForm);
          let fieldList = this.ticket.field_list;
          for (let i = 0; i < fieldList.length; i++) {
            for (let j = 0; j < detailFormKeys.length; j++) {
              if (
                [25, 30].includes(fieldList[i].field_type_id) &&
                fieldList[i].field_key === detailFormKeys[j]
              ) {
                this.detailForm[detailFormKeys[j]] = this.detailForm[
                  detailFormKeys[j]
                ].format("yyyy-MM-dd hh:mm:ss");
              }
            }
          }
          Object.assign(data.data, this.detailForm);
          this.submit(btn, data)
          this.$store
            .dispatch("api_patch_update_ticket", data)
            .then(resp => {
              // this.$Notice.success({ title: "保存成功" });
              // this.$router.push({ name: "todo" });
            })
            .catch(error => {
              this.$Notice.error({ title: "工单保存失败" });
              console.log(error);
            });
        } else {
          console.log("form error");
          return false;
        }
      });
      if (Object.keys(this.detailForm).length === 0) {
        let data = {
          id: this.ticket.id,
          data: {
            transition_id: btn.transition_id,
            suggestion: this.suggestion ? this.suggestion : btn.transition_name
          }
        };
        this.submit(btn, data)
      }
    }
  },
  computed: {
    ticket_id() {
      return this.$route.params.id;
    },
    displaySelectKey(argument) {
      return argument => {
        if (/35|45/.test(argument.field_type_id)) {
          return argument.field_choice[argument.field_value];
        }
        return argument.field_value;
      };
    },
    choiceFieldDisplay () {
      let result
      this.ticket.field_list.filter(item => {
        if (/35|45/.test(item.field_type_id)) {
          let keys = Object.keys(item.field_choice);
          for (let i = 0; i < keys.length; i++) {
            if (item.value === keys[i] || item.field_value === keys[i]) {
              result = item.field_choice[keys[i]];
            }
          }
          if (!result) {
            result = "——";
          }
        }
      });
      return result;
    },
    shortFieldList() {
      if (this.ticket && this.ticket.field_list) {
        let result = [];
        for (let i = 0; i < this.ticket.field_list.length; i++) {
          if (this.ticket.field_list[i].field_type_id === 55) {
            continue;
          } else {
            result.push(this.ticket.field_list[i]);
          }
        }
        this.ticket.field_list.map(item => {
          if (item.field_type_id === 55) {
            result.push(item);
          }
        });
        return result;
      }
    }
  },
  watch: {
    steps() {
      if (this.steps[0] && this.steps[0].state_id) {
        let current_order_id;
        let current = [];

        for (let i in this.steps) {
          if (this.steps[i].state_id == this.ticket.state_id) {
            current_order_id = this.steps[i].order_id;
          }
          current.push(this.steps[i].order_id);
        }

        current.sort();

        this.currentStep = current.indexOf(current_order_id);

        this.steps.filter(item => {
          // console.log(`${item.state_id} ---> ${this.ticket.state_id}`);
          if (item.state_id === this.ticket.state_id) {
            this.stepTransition = item;
          }
        });
      }
    },
    ticket() {
      let fieldList = this.ticket.field_list;
      for (let i = 0; i < fieldList.length; i++) {
        if (/2|3/.test(fieldList[i].field_attribute)) {
          // 动态设置detailForm表单默认值
          this.detailForm[fieldList[i].field_key] =
            fieldList[i].value || fieldList[i].field_value;
          // 动态设置detailForm表单验证
          if ([5, 35, 45, 55, 60].includes(fieldList[i].field_type_id)) {
            this.detailFormRules[fieldList[i].field_key] = [
              { required: true, type: "string", trigger: "blur" }
            ];
          } else if ([25, 30].includes(fieldList[i].field_type_id)) {
            this.detailFormRules[fieldList[i].field_key] = [
              { required: true, type: "date", trigger: "blur" }
            ];
          } else if ([40, 50, 70].includes(fieldList[i].field_type_id)) {
            this.detailFormRules[fieldList[i].field_key] = [
              { required: true, type: "array", trigger: "blur" }
            ];
          } else if ([10, 15].includes(fieldList[i].field_type_id)) {
            this.detailFormRules[fieldList[i].field_key] = [
              { required: true, type: "number", trigger: "blur" }
            ];
          } else if (fieldList[i].field_type_id === 20) {
            this.detailFormRules[fieldList[i].field_type_id] = [
              { required: true, type: "boolean", trigger: "blur" }
            ];
          } else if (fieldList[i].field_type_id === 80) {
            let value = fieldList[i].value || fieldList[i].field_value
            if(value) {
              this.fileList = [{
                name: value,
                url: value
              }]
            }
          } else if (fieldList[i].field_type_id === 90) {
            let value = fieldList[i].value || fieldList[i].field_value
            if(value) {
              this.imgFileList = [{
                name: value,
                url: value
              }]
            }
          }
        }
      }
    }
  },
  mounted() {
    this.init();
  }
};
</script>

<style scoped>
.ivu-form {
  font-size: 15px;
}
.ivu-form-item {
  margin-bottom: 4px;
  vertical-align: top;
  zoom: 1;
}
.disabled_field {
  overflow: hidden;
  display: inline-block;
  width: 100%;
  height: 100%;
  position: relative;
  line-height: 32px;
  color: rgba(0, 0, 0, 0.4);
}
</style>
