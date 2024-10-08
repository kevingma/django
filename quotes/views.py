from django.shortcuts import render
import random
# Create your views here.

quotes = [
    "We know we are alive and know we will die. We also know we will suffer during our lives before suffering—slowly or quickly—as we draw near to death. This is the knowledge we “enjoy” as the most intelligent organisms to gush from the womb of nature. And being so, we feel shortchanged if there is nothing else for us than to survive, reproduce, and die. We want there to be more to it than that, or to think there is. This is the tragedy: Consciousness has forced us into the paradoxical position of striving to be unself-conscious of what we are—hunks of spoiling flesh on disintegrating bones.",
    "This is the great lesson the depressive learns: Nothing in the world is inherently compelling. Whatever may be really “out there” cannot project itself as an affective experience. It is all a vacuous affair with only a chemical prestige. Nothing is either good or bad, desirable or undesirable, or anything else except that it is made so by laboratories inside us producing the emotions on which we live. And to live on our emotions is to live arbitrarily, inaccurately—imparting meaning to what has none of its own. Yet what other way is there to live? Without the ever-clanking machinery of emotion, everything would come to a standstill. There would be nothing to do, nowhere to go, nothing to be, and no one to know. The alternatives are clear: to live falsely as pawns of affect, or to live factually as depressives, or as individuals who know what is known to the depressive.",
    "Most people learn to save themselves by artificially limiting the content of consciousness."
    # "Nonexistence never hurt anyone. Existence hurts everyone.",
    # "Among the least praiseworthy incentives to reproduce are parents' pipe dreams of posterity - that egoistic compulsion to send emissaries into the future who will certify that their makers once lived and still live on, if only in photographs and home movies. Vying for an even less praiseworthy incentive to reproduce is the sometimes irresistible prospect of taking pride in one's children as consumer goods, trinkets, or tie-clips, personal accessories that may be shown off around town. But primary among the pressures to propagate is this: To become formally integrated into a society, one must offer it a blood sacrifice. As David Benatar has alleged in Better Never to Have Been, all procreators have blood-red hands, morally and ethically speaking.",
    # "Being alive is all right, so most of us say. But when death walks through the door, nothing is all right. As some believe that life is that which should not be, the bulk of the rest of us believe the same thing of death. That is its terror and its fascination. Everyone knows that we are all the dead-to-be. There are gegaws and knickknacks that stay in shape far longer than our mortal forms. If we called ourselves dead from the time we are born, we would not be far from the truth. But as long as we can walk or crawl or just lie abed sucking tubes, we can still say that being alive is all right.",
    # "Everything is engaged in a disordered fantasia of carnage. Everything tears away at everything else...forever.",
    # "Undeniably, one of the great disadvantages of consciousness–that is, consciousness considered as the parent of all horrors–is that it exacerbates necessary sufferings and creates unnecessary ones, such as the fear of death.",
    # "We are going to die, and that makes us the lucky ones. Most people are never going to die because they are never going to be born. The potential people who could have been here in my place but who will in fact never see the light of day outnumber the sand grains of Arabia. Certainly those unborn ghosts include greater poets than Keats, scientists greater than Newton. We know this because the set of possible people allowed by our DNA so massively exceeds the set of actual people. In the teeth of these stupefying odds it is you and I, in our ordinariness, that are here. We privileged few, who won the lottery of birth against all odds, how dare we whine at our inevitable return to that prior state from which the vast majority have never stirred?",
    # "To be alive is to inhabit a nightmare without hope of awakening to a natural world, to have our bodies embedded neck-deep in a quagmire of dread, to live as shut-ins in a house of horrors from which nobody gets out alive, and so on."
]

images = [
    "https://static.tvtropes.org/pmwiki/pub/images/thomas_ligotti.jpg",
    "https://static.wikia.nocookie.net/lovecraft/images/4/4c/Thomas_ligotti.jpg/revision/latest?cb=20210425041248",
    "https://socialecologies.wordpress.com/wp-content/uploads/2022/11/thomas_ligott_1.png",
    # "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhRMsL-u92I60jjRiLhm6KUlG2Hov6URqNnvXEcLdVRdFZPFBgKo6hshk1IRu_ksfta4qRrN0xgjnhd4ZjKnGM3p3Ic5eE5IBMRvf3i7XorloTj4fEDjLBJitNfJVWL1Lsj3Teo7sl5rh07/s640/Thomas+Ligotti.jpg"
]

def quote(request):
    """View for showing randomly selected quote"""
    quote_to_display = random.choice(quotes)
    image_to_display = random.choice(images)

    context = {
        'quote': quote_to_display,
        'image': image_to_display
    }

    return render(request, 'mini_fb/quote.html', context)

def show_all(request):
    """View for showing all quotes and images"""
    context = {
        'quotes': quotes,
        'images': images
    }
    return render(request, 'mini_fb/show_all.html', context)

def about(request):
    """View for information about quote author"""
    about_ligotti = "Thomas ligotti is an American author who is known for philosophical horror fiction. He has also written philosophical non-fiction - most of the quotes on this page are from his book 'The Conspiracy Against the Human Race.'"
    context = {
        'about_author': about_ligotti
    }
    return render(request, 'mini_fb/about.html', context)