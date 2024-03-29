complex_type2qa_examples = {
    "比较类": [
        {"q": "分子和原子的关系?", "a": "因为分子是保持物质化学性质的最小粒子， 而原子是化学变化中的最小粒子。所以分子由原子构成。", "class": "理学"},
        {"q": "矩阵和行列式的关系?", "a": "行列式是若干数字组成的一个类似于矩阵的方阵，矩阵的表示是用中括号，而行列式则用线段。 矩阵由数组成，而行列式是矩阵的所有不同行且不同列的元素之积的代数和。",
         "class": "理学"},
        {"q": "资本主义与社会主义的区别?", "a": "因为社会主义以生产资料公有制为基础，而资本主义以生产资料私有制为基础，所以资本主义与社会主义在生产资料的所有制形式上有本质区别。", "class": "社科"},
        {"q": "通货紧缩和通货膨胀的区别?",
         "a": "因为通货膨胀是指纸币的发行量超过流通中所需要的数量，从而引起纸币贬值、物价上涨的经济现象，其实质是社会总需求大于社会总供给；而通货紧缩是与通货膨胀相反的一种经济现象，是指在经济相对萎缩时期，物价总水平较长时间内持续下降，货币不断升值的经济现象，其实质是社会总需求持续小于社会总供给。",
         "class": "社科"},
        {"q": "栈和队列的相似点?", "a": "因为栈是只在表的同一端进行插入或删除操作的线性表，队列是只在表的一端进行插入或删除操作的线性表。所以,他们都可以在表的一端进行插入操作，并且都是线性表",
         "class": "工学"},
        {"q": "哈希表和数组的不同点?", "a": "因为哈希表是根据关键码值(Key value)而直接进行访问的数据结构，数组是有序的元素序列。所以，哈希表可以直接访问到关键码值对应的元素，而数组则不能",
         "class": "工学"},
        {"q": "儒家与道家的相同点?", "a": "因为道家以道为核心，认为大道无为、主张道法自然，而儒家注重人道大伦，以人性为主体。所以儒家与道家都是以道德为基础的治国理念，都是温和派", "class": "人文"},
        {"q": "洋务运动与戊戌变法的相同点?",
         "a": "因为洋务运动是晚清洋务派以“自强”、“求富”为口号利用西方军事装备、机器生产和科学技术以挽救清朝统治的自救运动。而戊戌变法是维新派人士通过光绪帝进行发展农、工、商业等的资产阶级改良运动。所以他们都是发生在清朝中后期的强国运动，都是为了维护清政府的统治。",
         "class": "人文"},
        {"q": "海湾战争与传统战争的区别?",
         "a": "因为传统空军的主要任务就是给地面部队提供支援，然后执行轰炸任务，但是在海湾战争中，空军形成了非常完整的作战体系。所以美空军在此次战役里把各种机型的特点和优势运用到了极致，让制空权的地位在战争中再次提升。",
         "class": "其他"},
        {"q": "内科与外科的区别?",
         "a": "因为内科主要是指疾病在经过检查、诊断之后，通常可以不需要进行手术治疗，绝大多数通过药物治疗就能够治疗好；而外科的疾病大多数是要通过手术来进行治疗的。所以内外科的主要区别在于治疗方式。",
         "class": "其他"},
    ],
    "举例类": [
        {"q": "宋词有哪些类型？", "a": "词根据全文字数可分为小令（58字以内）、中调（59字～90字）、长调（91字以上）。按照音乐性质可分为令、引、慢、三台、序子 、法曲、大曲、缠令、诸宫调九种。",
         "class": "人文"},
        {"q": "概率论的常用分布有哪些？", "a": "对离散型随机变量，有两点分布、二项分布、几何分布、泊松分布；对连续型随机变量，有均匀分布、指数分布、正态分布。", "class": "理学"},
        {"q": "有哪些字符串相关的算法？", "a": "字符串子串查找算法KMP、查找最长连续公共子序列的后缀数组算法、查找最长连续子序列的动态规划算法、利用状态机模糊匹配字符串。", "class": "工学"},
        {"q": "C++有什么好的课程吗？", "a": "入门C++可以观看《C++语言程序设计基础》，学完语法后可以学习《数据结构》中的算法。", "class": "工学"},
        {"q": "学习数据结构需要哪些基础知识?", "a": "高等数学方面，需要矩阵、多项式、极限和离散数学的基础知识；程序设计方面，需要至少一种编程语言的语法知识。", "class": "工学"},
        {"q": "职业体育获取经济效益的途径有哪些？", "a": "职业体育获取经济效益的途径有：商业赞助、赛事转播版权费、门票收入、销售纪念品等。", "class": "社科"},
        {"q": "摄影时有哪些好的构图技巧？", "a": "水平线构图、垂直线构图、斜线构图、S形曲线构图、散点式构图等。", "class": "其他"},
        {"q": "马克思主义政治经济学的基本原理有哪些？", "a": "马克思主义政治经济学基本原理包括四部分：劳动价值理论、剩余价值理论、再生产理论、资本主义发展理论。", "class": "社科"}
    ],
    "方法类": [
        {"q": "时间复杂度怎么算?",
         "a": "首先，将时间复杂度理解为算法中各条指令的执行时间之和，将各条指令分解为若干次如算术运算，比较，分支等基本操作，认为每一次这类基本操作都可在常数时间内完成，如此，定义T(n)为算法所执行基本操作的总次数，按照上述分析，只需统计出该算法所执行基本操作的总次数，即可计算出时间复杂度。",
         "class": "工学"},
        {"q": "十进制数转二进制数怎么转换?",
         "a": "首先用2整除十进制整数，可以得到一个商和余数；再用2去除商，又会得到一个商和余数，如此进行，直到商为小于1时为止，然后把先得到的余数作为二进制数的低位有效位，后得到的余数作为二进制数的高位有效位，依次排列起来，就得到对应的二进制数。",
         "class": "理学"},
        {"q": "中央银行如何利用不同的货币政策来调节经济?",
         "a": "在不同的经济形势下，中央银行要运用不同的货币政策来调节经济。在萧条时期，总需求小于总供给，为了刺激总需求，就要利用扩张性的货币政策。其中包括在公开市场上买进有价证券，降低贴现率并放松贴现条件，降低准备率等。在繁荣时期，总需求大于总供给，为了抑制总需求，就要运用紧缩性货币政策，包括在公开市场上卖出有价证券，提高贴现率并严格贴现条件，提高准备率等。",
         "class": "社科"},
        {"q": "如何进行实证研究?", "a": "首先提出假设，然后收集客观数据，最后通过数据分析结果，接受或拒绝假设。", "class": "社科"},
        {"q": "如何鉴赏宋词?", "a": "鉴赏宋词，首先要欣赏宋词的意境美，从领略、把握宋词的意境入手，理解宋词深邃、优美的境界。其次，要欣赏宋词的语言美。此外，要欣赏宋词的形式美，欣赏它规整的格式",
         "class": "人文"},
        {"q": "如何结合20世纪20、30年代的具体国情对马列主义意识形态作出转化与创新?",
         "a": "首先，必须修改“无产阶级”的定义——把农民中具有小农和雇佣劳动力双重角色的这一阶层从理论上划为无产阶级或半无产阶级。其次，还须对马列主义的夺取政权的理论进行修改，确立在农村建党建政的合理性。",
         "class": "人文"},
        {"q": "如何有效地领导自己", "a": "第一、不断地自我反省；第二、永远保持一个开放的心态，愿意去探索新的东西；第三、主动寻求别人有建设性的反馈意见；第四、拥抱挑战、拥抱挫折。", "class": "其他"},
        {"q": "遇到有毒气体应当采取哪些防护措施?", "a": "应当通过戴面具、口罩，用浸渍碱水的毛巾捂住口鼻的方式阻止毒气吸入，向侧风方向撤离，并采取对症治疗。", "class": "其他"}
    ],
    "原因类": [
        {"q": "为什么温度计要甩一甩?",
         "a": "因为水银比热容较低,对温度变化敏感,所以设计体温计时,如果没有外力,水银柱只能上升不能下降。再次使用时用力甩几下,水银柱就会降回原来的位置,量的体温才会准确。", "class": "理学"},
        {"q": "地心说为什么是错的?",
         "a": "因为如果以地球为中心，那么其它天体的运动看起来是杂乱无章的，但是以太阳为中心的话，行星包括地球在内的运动是简单的椭圆。哥白尼最初的观点是对奥卡姆剃刀的应用，他认为越简单越好，所以太阳一定在中心，因此地心说错误。",
         "class": "理学"},
        {"q": "剩余价值为什么会转化为利润?",
         "a": "因为1、资本家预付的不变资本和可变资本采取了生产成本的形态，在生产成本形态上，可变资本的特殊作用，即作为剩余价值的唯一源泉被模糊了。剩余价值被看作是全部预付资本的产物。 2、劳动力的价值采取了工资形式。",
         "class": "社科"},
        {"q": "为什么货币会贬值?", "a": "因为1、货币的价值是和商品挂钩的。 2、如果货币的发行量超过了商品的数量，那么货币就会贬值，外在表现为价格上升，货币贬值。", "class": "社科"},
        {"q": "嵌入式底层开发为什么选择C语言?",
         "a": "因为1、良好的移植性：C语言在不同的软件平台，拥有相同的语法。在不同的硬件平台下同样适用。所以C语言可以在不同的软硬平台，进行很好地移植。2、直接访问硬件： C语言中，我们可以通过指针控制内存以及寄存器。3、运行效率高:C程序运行效率可达汇编的80%，而其它程序可能只有C程序的80%。",
         "class": "工学"},
        {"q": "为什么说操作系统是用户和计算机的接口？",
         "a": "因为1、操作系统中提供了底层交换，包括一些硬件的整合，也是通过操作系统来进行交换，单纯靠软件是无法直接与硬件交互的。2、操作系统提供了一个人机操作界面，使用用户可以通过操作系统从而利用硬件资源来进行一些资源整合和计算，所以说操作系统也是用户与计算机之间的接口。",
         "class": "工学"},
        {"q": "古罗马为什么灭亡?", "a": "因为1、落后的奴隶生产方式严重阻碍了经济的进步。2、破碎的军权转换机制大大影响了军事的强大。3、日耳曼人的入侵成为了帝国灭亡的最后一步。", "class": "人文"},
        {"q": "为什么新中国的成立开辟了新纪元?",
         "a": "因为1、从革命任务看：中国人民经过一百多年的英勇斗争，终于推翻了帝国主义、封建主义和官僚资本主义的统治，取得新民主主义革命的基本胜利。2、从国家发展看：新中国的成立，开辟了中国历史的新纪元，中国进入了人民当家做主的新时代。3、从世界角度看：新中国的成立，是20世纪世界上发生的最有影响的伟大事件之一。",
         "class": "人文"},
        {"q": "为什么癌症很难治愈?",
         "a": "通常癌症很难治愈,是由于癌症细胞特有的生物学行为特点所决定。癌症在生长、增殖过程中,常会发生对周围组织的侵袭、浸润,甚至是发生转移等情况。在手术切除之后,癌症也常会出现复发的现象,也就导致了癌症比较难以治愈。",
         "class": "其他"},
        {"q": "孙子兵法为什么现在还有意义?",
         "a": "在现代社会里，经典的东西依然会继续传承，因为它被漫长的历史深刻检验了，证明了它是正确有用的。就如《孙子兵法》这本书一样，它经历了无数场战争的考验，并且通过了，所以它能流传到现在还一直在被各种人学习，不只是军事谋略，还有很多其他的，所以它现在还是有实战意义的。",
         "class": "其他"},
    ],
    "random": [
        {"q": "如何有效地领导自己", "a": "第一、不断地自我反省；第二、永远保持一个开放的心态，愿意去探索新的东西；第三、主动寻求别人有建设性的反馈意见；第四、拥抱挑战、拥抱挫折。", "class": "其他"},
        {"q": "资本主义与社会主义的区别?", "a": "因为社会主义以生产资料公有制为基础，而资本主义以生产资料私有制为基础，所以资本主义与社会主义在生产资料的所有制形式上有本质区别。", "class": "社科"},
        {"q": "如何进行实证研究?", "a": "首先提出假设，然后收集客观数据，最后通过数据分析结果，接受或拒绝假设。", "class": "社科"},
        {"q": "古罗马为什么灭亡?", "a": "因为1、落后的奴隶生产方式严重阻碍了经济的进步。2、破碎的军权转换机制大大影响了军事的强大。3、日耳曼人的入侵成为了帝国灭亡的最后一步。", "class": "人文"},
    ]
}
