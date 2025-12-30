class Form4 extends Component {
  static props = ['state', 'data']

  setup() {
    this.state = useState({
      formData: {
        document_1: null,
        document_2: null,
        document_3: null,
        document_4: null,
        document_5: null,
        document_6: null,
        document_7: null,
        document_8: null,
        document_9: null,
        document_10: null,
        document_11: null,
        document_12: null,
        document_13: null,
        document_14: null,
        document_15: null,
        document_16: null,
      },
      files_errors: {
        document_1_error: null,
        document_2_error: null,
        document_3_error: null,
        document_4_error: null,
        document_5_error: null,
        document_6_error: null,
        document_7_error: null,
        document_8_error: null,
        document_9_error: null,
        document_10_error: null,
        document_11_error: null,
        document_12_error: null,
        document_13_error: null,
        document_14_error: null,
        document_15_error: null,
        document_16_error: null,
      },
    })
  }

  handleChange(event) {
    const { state } = this.props
    const { name, files } = event.target
    this.state.files_errors[name + '_error'] = null
    const file = files[0]

    if (file) {
      if (file.type !== 'application/pdf') {
        this.state.files_errors[name + '_error'] = 'الرجاء تحميل ملف PDF فقط.'
        state.formData[name] = null
        event.target.files = null
        return
      }

      if (file.size > 1048576) {
        this.state.files_errors[name + '_error'] = 'حجم الملف يجب أن لا يتجاوز 1 ميغابايت.'
        state.formData[name] = null
        event.target.files = null
        return
      }

      if (this.state.files_errors[name + '_error'] == null) {
        state.formData[name] = file
      }
    } else {
      state.formData[name] = null
    }
  }

  static template = xml`
<label for="documents" style="font-size: 16px; font-weight:bold; color: #045444;">
    اضف المستندات التالية
</label>

<table id="documents_table" class="table">
    <tbody id="documents">
        <tr>
            <td>
                <span>
                    طلب التسهيلات ممضي من طرف المفوض القانوني عن الشركة <span class="field-require">*</span>
                </span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_1" name="document_1" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_1_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_1_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>
                    الميزانيات لثلاث سنوات السابقة مصادق عليها من طرف المدقق المحاس <span class="field-require">*</span>
                </span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_2" name="document_2" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_2_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_2_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>
                    الميزانية الافتتاحية و الميزانية المتوقعة للسنة المراد تمويلها موقعة من طرف
                    الشركة (حديثة النشأة)
                </span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_3" name="document_3" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_3_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_3_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>
                    مخطط تمويل الاستغلال مقسم الى أرباع السنة للسنة المراد تمويلها
                </span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_4" name="document_4" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_4_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_4_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>
                    المستندات و الوثائق المتعلقة بنشاط الشركة ( عقود، صفقات ، طلبيات ، ... )
                </span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_5" name="document_5" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_5_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_5_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>
                    محاضر الجمعيات العادية و الغير العادية للأشخاص المعنويين
                </span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_6" name="document_6" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_6_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_6_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>
                    نسخة مصادق عليها من السجل التجاري <span class="field-require">*</span>
                </span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_7" name="document_7" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_7_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_7_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>نسخة مصادق عليها من القانون الأساسي للشركة <span class="field-require">*</span></span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_8" name="document_8" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_8_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_8_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>مداولة الشركاء أو مجلس الإدارة لتفويض المسير لطلب القروض البنكية</span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_9" name="document_9" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_9_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_9_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>نسخة مصادق عليها من النشرة الرسمية للإعلانات القانونية</span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_10" name="document_10" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_10_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_10_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>نسخة طبق الأصل لعقد ملكية أو استئجار المحلات ذات الاستعمال المهني</span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_11" name="document_11" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_11_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_11_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>نسخة طبق الأصل للشهادات الضريبية و شبه الضريبية حديثة (أقل من ثلاثة
                    أشهر) <span class="field-require">*</span>
                </span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_12" name="document_12" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_12_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_12_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>استمارة كشف مركزية المخاطر ممضية من طرف ممثل الشركة (نموذج مرفق) <span class="field-require">*</span></span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_13" name="document_13" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_13_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_13_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>آخر تقرير مدقق الحسابات</span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_14" name="document_14" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_14_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_14_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>Actif, Passif, TCR (N, N-1) <span class="field-require">*</span></span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_15" name="document_15" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_15_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_15_error"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <span>Actif, Passif, TCR (N-2, N-3) <span class="field-require">*</span></span>
            </td>
            <td>
                <input type="file" t-on-change="handleChange"
                       class="form-control form-control-sm custom-file-input"
                       id="document_16" name="document_16" accept="application/pdf"/>
            </td>
        </tr>
                <tr t-if="state.files_errors.document_16_error" >
            <td colspan="2">
                <div class="alert alert-danger m-1" role="alert">
                    <t t-esc="state.files_errors.document_16_error"/>
                </div>
            </td>
        </tr>
    </tbody>
</table>

    `
}
