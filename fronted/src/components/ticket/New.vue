<template>
  <!-- TODO: ElementUI/iView对于动态v-model都有BUG，改用单选菜单方式 -->
  <!-- <el-radio-group v-if="item.field_type_id === 35" v-model="newForm[item.field_key]">
    <el-radio v-for="(choice, i) in Object.keys(item.field_choice)" :key="i" :label="choice">{{item.field_choice[choice]}}</el-radio>
  </el-radio-group> -->
  <!-- <RadioGroup v-if="item.field_type_id === 35" v-model="newForm[item.field_key]">
    <Radio v-for="(choice, i) in Object.keys(item.field_choice)" :key="i" :label="choice">{{item.field_choice[choice]}}</Radio>
  </RadioGroup> -->
  <div class="container">
    <div class="select-workflow-con">
      <Card style="text-align: left;">
        <template slot="title"><span style="font-weight: 700;">选择业务</span></template>
        <Select v-model="workflow" size="large" label-in-value @on-change="handleWorkflow" style="width: 400px;">
          <Option v-for="(item, index) in workflows" :key="index" :value="item.id">{{item.name}}</Option>
        </Select>
      </Card>
    </div>
    <div class="new-form-con" v-if="workflow">
      <Card style="text-align: left;">
        <template slot="title" v-cloak><span style="font-weight: 700;">{{ workflowTitle }}</span></template>
        <div class="form" v-if="!fieldEmpty">
          <Form ref="newForm" :model="newForm" :rules="newFormRules" :label-width="150">
            <Row>
              <Col :md="{span: item.field_type_id === 55 ? 22 : 11}" v-for="(item, index) in init_state.field_list" :key="index">
                <FormItem :label="item.name || item.field_name" :prop="item.field_key">
                  <Input v-if="item.field_type_id === 5" v-model="newForm[item.field_key]" :placeholder="$t(`field_label.${item.field_key}`)"/>
                  <InputNumber v-if="item.field_type_id === 15" v-model="newForm[item.field_key]" :min="0" :step="0.5" style="width: 100%;"></InputNumber>
                  <DatePicker v-if="item.field_type_id === 30" v-model="newForm[item.field_key]" type="datetime" format="yyyy-MM-dd HH:mm:ss" style="width: 100%;" :placeholder="$t(`field_label.${item.field_key}`)"></DatePicker>
                  <Select v-if="item.field_type_id === 40" v-model="newForm[item.field_key]" multiple :placeholder="$t(`field_label.${item.field_key}`)">
                    <Option v-for="(choice, i) in Object.keys(item.field_choice)" :key="i" :value="choice">{{item.field_choice[choice]}}</Option>
                  </Select>
                  <Select v-if="item.field_type_id === 45 || item.field_type_id === 35" v-model="newForm[item.field_key]" :placeholder="$t(`field_label.${item.field_key}`)">
                    <Option v-for="(choice, i) in Object.keys(item.field_choice)" :key="i" :value="choice">{{item.field_choice[choice]}}</Option>
                  </Select>

                  <ueditor v-if="item.field_type_id === 55" @ready="handleReady" :field_key="item.field_key"></ueditor>
                  <Select v-if="item.field_type_id === 60" v-model="newForm[item.field_key]" :placeholder="$t(`field_label.${item.field_key}`)">
                    <Option v-for="(user, index) in accountList" :key="index" :value="user.username">{{user.alias}}</Option>
                  </Select>
                  <Select v-if="item.field_type_id === 70" v-model="newForm[item.field_key]" multiple :placeholder="$t(`field_label.${item.field_key}`)">
                    <Option v-for="(user, index) in accountList" :key="index" :value="user.username">{{user.alias}}</Option>
                  </Select>
                  <el-upload
                    v-if="item.field_type_id === 80"
                    action="/api/v1/service/ueditor/?action=uploadfile&encode=utf-8"
                    :on-success="onsuccess"
                    :on-remove="onremove"
                    name="upfile"
                    :file-list="getFileList(item)">
                    <Button type="primary" size="small" @click="getItem(item)">点击上传</Button>
                  </el-upload>
                  <el-upload
                    @click.native="getItem(item)"
                    v-if="item.field_type_id === 90"
                    action="/api/v1/service/ueditor/?action=uploadimage"
                    :on-success="onsuccess"
                    :on-remove="onremove"
                    :on-preview="onpreview"
                    accept="image/*"
                    name="upfile"
                    list-type="picture-card"
                    :file-list="getFileList(item)">
                    <i class="el-icon-plus"></i>
                  </el-upload>
                  <el-dialog
                    v-if="item.field_type_id === 90"
                    :visible.sync="Dialog" 
                    :modal="false"
                    top="10vh">
                    <img width="100%" :src="imgSrc" alt="图片">
                  </el-dialog>
                </FormItem>
              </Col>
            </Row>
            <FormItem style="text-align: center;">
              <Button v-for="(btn, b) in init_state.transition" :key="b" @click="handleButton('newForm', btn.transition_id)" :type="btn.transition_id === 1 ? 'primary' : 'info'" style="margin: 0 5px;">{{btn.transition_name}}</Button>
              <!-- <Button type="warning" style="margin: 0 5px;" @click="reset('newForm')">重置</Button> -->
            </FormItem>
          </Form>
        </div>
        <div class="form" v-else>
          <span>业务流程未初始化配置</span>
        </div>
      </Card>
    </div>
    <Spin fix v-if="loading">
      <Icon type="load-c" size=50 class="demo-spin-icon-load"></Icon>
      <div style="font-size: 28px;">loading...</div>
    </Spin>
  </div>
</template>

<script>
import Validators from '../../utils/validators'
import {Date} from '../../utils/datetime'
import ueditor from './components/ueditor'

export default {
  name: 'new',
  components: {
    ueditor
  },
  data () {
    return {
      loading: false,
      workflows: [],
      accountList: [],
      workflow: null,
      init_state: {},
      workflowTitle: '',
      ueditorConfig: {},
      Dialog: false,
      item: {},
      imgSrc: ''
    }
  },
  methods: {
    getFileList (item) {
      let data = item.field_value || item.default_value
      if (data) {
        if(Array.isArray(data)) {
          return data
        } else {
          return JSON.parse(data)
        }
      }
      return []
    },
    getItem (item) {
      this.item = item
    },
    onsuccess (response, file, fileList) {
      if (response.state != 'SUCCESS') {
        this.$Notice.error({title: '上传失败'})
        let index = fileList.findIndex(i => i.name == file.name)
        fileList.splice(index, 1)
      }
      this.item.field_value = fileList
    },
    onremove (file, fileList) {
      let arr = this.init_state.field_list
      for(let i = 0; i < arr.length; i++) {
        if(Array.isArray(arr[i].field_value)) {
          let index = arr[i].field_value.findIndex(i => i.name == file.name)
          if(index >= 0) {
            fileList.splice(index, 1)
            arr[i].field_value.splice(index, 1)
          }
        }
      }
    },
    onpreview (file) {
      this.Dialog = true
      this.imgSrc = file.url
    },
    init () {
      this.loading = true
      this.$store.dispatch('api_workflows').then(resp => {
        this.workflows = resp.data.data.value
        this.loading = false
      })
    },
    handleWorkflow (workflow) {
      this.workflowTitle = workflow.label
      this.workflow = workflow.value
      this.loading = true
      this.$store.dispatch('api_init_state', {id: workflow.value}).then(resp => {
        this.init_state = resp.data.data
        if (this.init_state.field_list) {
          this.$store.dispatch('api_fetch_account_list').then(resp => {
            this.accountList = resp.data.data
            this.loading = false
          })
        }
        this.loading = false
      })
    },
    handleButton (formName, id) {
      this.$refs[formName].validate(valid => {
        if (!valid) return
        let data = {
          workflow_id: this.workflow,
          transition_id: id
        }
        Object.assign(data, this.newForm)
        for (let i = 0; i < Object.keys(this.init_state.field_list).length; i++) {
          let item = this.init_state.field_list[i]
          if ([25, 30].includes(item.field_type_id)) {
            data[item.field_key] = data[item.field_key].format("yyyy-MM-dd hh:mm:ss")
          }
          if ([70].includes(item.field_type_id)) {
            data[item.field_key] = data[item.field_key].join(',')
          }
          if ([80, 90].includes(item.field_type_id)) {
            let arr = item.field_value.map(i => {
              return {
                name: i.name,
                url: i.response.url
              }
            })
            console.log(arr)
            data[item.field_key] = JSON.stringify(arr)
          }
        }
        this.$store.dispatch('api_post_ticket', data).then(resp => {
          this.$Notice.success({title: '创建成功'})
          this.$router.push({name: 'myself'})
        }).catch(error => {
          this.$Notice.error({title: '创建失败'})
        })
      })
    },
    handleReady (instance, field_key) {
      instance.setContent('')
      instance.addListener('contentChange', () => {
        this.newForm[field_key] = instance.getContent()
      })
    },
    reset (formName) {
      this.$refs[formName].resetFields()
    }
  },
  computed: {
    fieldEmpty () {
      for (let i in this.init_state.field_list) {
        return false
      }
      return true
    },
    newFormRules () {
      let validators = {}
      this.init_state.field_list.map(item => {
        if (item.field_attribute === 2) {
          if ([5, 35, 45, 55, 60].includes(item.field_type_id)) {
            validators[item.field_key] = [{validator: Validators.string, type: 'string', trigger: 'blur'}]
          } else if ([25, 30].includes(item.field_type_id)) {
            validators[item.field_key] = [{validator: Validators.datetime, type: 'date', trigger: 'blur'}]
          } else if ([40, 50, 70].includes(item.field_type_id)) {
            validators[item.field_key] = [{required: true, type: 'array', trigger: 'blur'}]
          } else if ([10, 15].includes(item.field_type_id)) {
            validators[item.field_key] = [{validator: Validators.number, type: 'number', trigger: 'blur'}]
          } else if (item.field_type_id === 20) {
            validators[item.field_type_id] = [{required: true, type: 'boolean', trigger: 'blur'}]
          }
        }
      })
      return validators
    },
    newForm () {
      let form = {}
      let list = this.init_state.field_list
      let value
      for (let i = 0; i < list.length; i++) {
        if ([40, 50, 70].includes(list[i].field_type_id)) {
          value = []
        } else if ([10, 15].includes(list[i].field_type_id)) {
          value = 0
        } else {
          value = ''
        }
        form[list[i].field_key] = list[i].default_value || value
      }
      return form
    }
  },
  created () {
    this.init()
  }
}
</script>

<style lang="less" scoped>
.new-form-con {
  margin-top: 15px;
}
</style>
